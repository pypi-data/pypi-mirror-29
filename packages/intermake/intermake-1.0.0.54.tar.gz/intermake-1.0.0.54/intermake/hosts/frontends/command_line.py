"""
Provides a command-line based front-end.

This is only a simple front end for executing basic commands from the command line - for scripting, the Python Interactive Interface provides a similar interface with more features.
(Python Interactive is invoked by calling code.interact, see :function:`pyi`). 
"""
import os
import shlex
import sys
import warnings
from os import path
from typing import Callable, Dict, Iterator, List, Optional, Tuple

from intermake.engine import constants
from intermake.engine.constants import EStream
from intermake.engine.environment import MENV, MCMD
from intermake.engine.plugin import Plugin, PluginArg
from intermake.engine.theme import Theme
from intermake.hosts.base import ERunMode
from intermake.hosts.console import UserExitError, ConsoleHost
from mhelper import FindError, ansi_format_helper, file_helper, string_helper, ansi


__author__ = "Martin Rusilowicz"

__save_history_function: Callable[[], None] = None
__iter_history_function: Callable[[], Iterator[str]] = None
__clf_settings: "_CommandLineFrontendSettings" = None
__clf_configuration: "_CommandLineFrontendSettings" = None


class _CommandLineFrontendSettings:
    """
    Settings used by the Command Line frontend.
    
    :attr error_traceback        : Normally error details are suppressed but can be displayed using the
                                   `error` command.
                                   When this setting is on, the full traceback is always printed as soon as
                                   an error occurs.
    :attr args_invokes_cli:      : Always invoke the CLI after the command line arguments have been processed..
    :attr error_invokes_cli:     : Normally, an error in ARG mode causes the application to exit.
                                   When this setting is on, an error in ARG mode starts the CLI instead (like Paup).
    """
    
    
    def __init__( self ):
        self.error_traceback = False
        self.args_invokes_cli = False
        self.error_invokes_cli = False
        self.aliases = { }


def get_clf_settings() -> Tuple[_CommandLineFrontendSettings, _CommandLineFrontendSettings]:
    global __clf_settings, __clf_configuration
    
    if __clf_settings is None:
        __clf_settings = MENV.local_data.store.bind( "cli_frontend", _CommandLineFrontendSettings() )
        __clf_configuration = _CommandLineFrontendSettings()
    
    return __clf_settings, __clf_configuration


def iter_history():
    return __iter_history_function()


def find_command( text: str, plugin_type: type = None ):
    """
    Finds the command with the name.
    :param text: 
    :param plugin_type: 
    :return:
    :except FindError: Find failed. 
    """
    source_list = MENV.plugins.all_plugins()
    
    if plugin_type:
        source_list = [x for x in source_list if isinstance( x, plugin_type )]
    
    host = MENV.host
    text = host.translate_name( text )
    
    
    def ___get_names( plugin: Plugin ):
        return [host.translate_name( x ) for x in plugin.names]
    
    
    return string_helper.find( source = source_list,
                               search = text,
                               namer = ___get_names,
                               detail = "plugin",
                               fuzzy = True )


class CliSyntaxError( Exception ):
    """
    Syntax error of the CLI.
    """
    pass


def __execute_command( arguments: List[str] ) -> None:
    """
    Executes a command
    
    :param arguments: See `Plugins.Commands.general_help()` for a description of what is parsed. 
    """
    # No arguments means do nothing
    if len( arguments ) == 0 or (len( arguments ) == 1 and not arguments[0]):
        return
    
    # ":" and "then" mean we will perform 2 commands, so split about the ":" and repeat
    delimiters = (":", "then")
    
    for delimiter in delimiters:
        if delimiter in arguments:
            i = arguments.index( delimiter )
            left = arguments[0:i]
            right = arguments[(i + 1):]
            __execute_command( left )
            __execute_command( right )
            return
    
    # Get the command name (first argument)
    cmd = arguments[0]
    
    arguments = arguments[1:]
    
    # Find the plugin we are going to run
    try:
        plugin = find_command( cmd )  # type: Plugin
    except FindError as ex:
        raise CliSyntaxError( "The plugin «{}» does not exist.".format( cmd ) ) from ex
    
    # Create the parameters
    args = []  # type: List[Optional[object]]
    kwargs = { }  # type: Dict[str,Optional[object]]
    
    host = MENV.host
    
    for arg_text in arguments:
        # "+" and "~" mean assign a keyword argument to True/False.
        # I didn't permit "-" because this is ambiguous between a minus (which would imply False) and a Unix parameter (which would imply True).
        # and I didn't permit "/" because this is ambiguous between a Windows parameter (which would imply True) and a path on Unix (which is something else).
        if arg_text.startswith( "+" ):
            arg_text = arg_text[1:] + "=True"
        elif arg_text.startswith( "~" ):
            arg_text = arg_text[1:] + "=False"
        
        # "=" means a keyword argument
        if "=" in arg_text:
            k, v = arg_text.split( "=", 1 )
            if k in kwargs:
                raise CliSyntaxError( "The key «{0}» has been specified more than once.".format( k ) )
            
            try:
                plugin_arg = string_helper.find(
                        source = plugin.args,
                        search = host.translate_name( k ),
                        namer = lambda x: host.translate_name( x.name ),
                        detail = "argument" )  # type: PluginArg
            except FindError as ex:
                raise CliSyntaxError( "Cannot find argument «{}» in «{}».".format( k, plugin ) ) from ex
            
            if plugin_arg is None:
                raise CliSyntaxError( "The plugin «{}» does not have an argument named «{}» or similar. The available arguments are: {}".format( plugin.name, k, ", ".join( x.name for x in plugin.args ) ) )
            
            kwargs[plugin_arg.name] = __convert_string( plugin_arg, plugin, v )
        else:
            # Everything else is a positional argument
            if kwargs:
                raise CliSyntaxError( "A positional parameter (in this case «{0}») cannot be specified after named parameters.".format( arg_text ) )
            
            if len( args ) == len( plugin.args ):
                raise CliSyntaxError( "Too many arguments specified for «{}», which takes {}.".format( plugin, len( plugin.args ) ) )
            
            plugin_arg = plugin.args[len( args )]
            
            args.append( __convert_string( plugin_arg, plugin, arg_text ) )
    
    plugin.run( *args, **kwargs )


def __convert_string( arg, plugin, value: str ):
    value = string_helper.unescape( value )
    
    import stringcoercion
    try:
        result = stringcoercion.get_default_coercer().coerce( arg.type, value )
        return result
    except Exception as ex:
        raise CliSyntaxError( "Value «{}» rejected for argument «{}» on plugin «{}». See causing error for details.".format( value, arg, plugin ) ) from ex


def __begin_readline() -> Optional[Callable[[], None]]:
    """
    Starts readline (the root that allows a UNIX terminal to accept things besides basic text).
    It doesn't work on Windows, or even some UNIX some platforms, which is why its got to be quarantined here.
    Returns a function that can be called to save the history on program termination.
    """
    global __save_history_function, __iter_history_function
    
    if __save_history_function is not None:
        # Already started
        return
    
    # noinspection PyBroadException
    try:
        import readline
    except:  # don't know, don't care, it doesn't work, carry on
        __save_history_function = lambda: None
        __iter_history_function = lambda: []
        return
    
    history_file = os.path.join( MENV.local_data.local_folder( constants.FOLDER_SETTINGS ), "command-history.txt" )
    
    
    class __Completer:
        """
        Used by readline to manage autocompletion of the command line.
        """
        
        
        def __init__( self ):
            """
            Constructor.
            """
            self.matches = []
            self.keywords = [MENV.host.translate_name( x.name ) for x in MENV.plugins.all_plugins() if x.is_visible]
        
        
        def complete( self, text: str, state: int ) -> Optional[str]:
            """
            See readline.set_completer.
            """
            if state == 0:
                self.matches = [x for x in self.keywords if text in x]
            
            if state < 0 or state >= len( self.matches ):
                return None
            else:
                return self.matches[state]
        
        
        # noinspection PyUnusedLocal
        def show( self, substitution: str, matches: List[str], longest_match_length: int ) -> None:
            """
            See readline.set_completion_display_matches_hook.
            """
            host = MENV.host
            MCMD.print( "", stream = EStream.SYSTEM )
            MCMD.print( Theme.COMMAND_NAME + str( len( matches ) ) + Theme.RESET + " matches for " + Theme.COMMAND_NAME + substitution + Theme.RESET + ":", stream = EStream.SYSTEM )
            
            if len( self.matches ) > 10:
                MCMD.print( "Maybe you meant something a little less ambiguous...", stream = EStream.SYSTEM )
            else:
                for x in self.matches:
                    MCMD.print( "Command " + Theme.COMMAND_NAME + str( x ) + Theme.RESET, stream = EStream.SYSTEM )
    
    
    if history_file:
        if path.isfile( history_file ):
            try:
                readline.read_history_file( history_file )
            except Exception:
                warnings.warn( "Error using history file «{}». This may be a version incompatibility. History not loaded and the file will be overwritten.".format( history_file ) )
    
    readline.parse_and_bind( 'tab: complete' )
    readline.parse_and_bind( 'set show-all-if-ambiguous on' )
    completer = __Completer()
    readline.set_completer( completer.complete )
    # readline.set_completion_display_matches_hook( completer.show )
    readline.set_completer_delims( " " )
    
    
    def __write_history_file():
        if history_file:
            try:
                readline.write_history_file( history_file )
            except Exception as ex:
                raise IOError( "Failed to write the history file to «{}».".format( history_file ) ) from ex
    
    
    def iter_history():
        for i in range( readline.get_current_history_length() ):
            yield readline.get_history_item( i + 1 )
    
    
    __save_history_function = __write_history_file
    __iter_history_function = iter_history


def start_cli( read_argv: bool ) -> None:
    """
    Starts the CLI frontend.
    
    This operates in two modes, the first reads the command line arguments from `sys.argv`, and the second takes user input using `input`.
    
    Generally the host will be a `ConsoleHost` instance, though other hosts are tolerated.
    
    :param read_argv: When `True`, reads command line arguments.
    """
    from intermake.hosts.console import ConsoleHost
    from intermake.plugins import common_commands
    from intermake.engine import cli_helper
    __begin_readline()
    
    clf_settings, clf_config = get_clf_settings()
    
    # Run the startup arguments
    queue = []
    
    if read_argv:
        for index, arg in enumerate( sys.argv[1:] ):
            if index == 0 and arg in ("--help", "-help", "/help", "-?", "/?"):
                queue.append( "help" )
            elif arg.startswith( "--" ):
                queue.append( ":" )
                queue.append( arg[2:] )
            else:
                queue.append( arg )
        
        if len( queue ) > 1:
            queue = [" ".join( '"{}"'.format( x ) if " " in x else x for x in queue )]
        
        if not queue:
            common_commands.start_ui( ERunMode.CLI )
            return
        
        print( cli_helper.format_banner( "Command Line Arguments", MENV.abv_name + " help", MENV.abv_name + " cmdlist" ) )
    else:
        print( cli_helper.format_banner( "Command Line Interactive", "help", "cmdlist" ) )
    
    try:
        while True:
            if read_argv:
                if not queue:
                    if clf_settings.args_invokes_cli:
                        MCMD.print( "Note: CLI starting because `args_invokes_cli` is set." )
                        common_commands.start_ui( ERunMode.CLI )
                    elif clf_config.args_invokes_cli:
                        common_commands.start_ui( ERunMode.CLI )
                    
                    raise UserExitError( "ARGV executor requesting exit; all arguments parsed." )
                
                x = queue.pop( 0 )
            else:
                x = __read_arg()
            
            try:
                execute_text( x )
            except KeyboardInterrupt as ex:
                MCMD.print( Theme.WARNING + "-------------------------------------------------" + Theme.RESET, stream = EStream.SYSTEM )
                MCMD.print( Theme.WARNING + "- KEYBOARD INTERRUPT - OUTPUT MAY BE INCOMPLETE -" + Theme.RESET, stream = EStream.SYSTEM )
                MCMD.print( Theme.WARNING + "-------------------------------------------------" + Theme.RESET, stream = EStream.SYSTEM )
                
                if clf_settings.error_traceback or clf_config.error_traceback or read_argv:
                    MCMD.print( ansi_format_helper.format_traceback( ex ), stream = EStream.SYSTEM )
            except Exception as ex:
                if clf_settings.error_traceback or clf_config.error_traceback or read_argv:
                    MCMD.print( ansi_format_helper.format_traceback( ex ), stream = EStream.SYSTEM )
                
                ex_msg = str( ex )
                ex_msg = string_helper.highlight_quotes( ex_msg, "«", "»", Theme.ERROR_BOLD, Theme.ERROR )
                MCMD.print( Theme.ERROR + ex_msg + Theme.RESET, stream = EStream.ERROR )
                
                if read_argv and (clf_settings.error_invokes_cli or clf_config.error_invokes_cli):
                    MCMD.print( Theme.WARNING + "---------------------------------------------------------" + Theme.RESET, stream = EStream.SYSTEM )
                    MCMD.print( Theme.WARNING + "- CURRENT SETTINGS DICTATE THAT THE CLI STARTS ON ERROR -" + Theme.RESET, stream = EStream.SYSTEM )
                    MCMD.print( Theme.WARNING + "- use the {}local{} command to modify this functionality    -".format( Theme.WARNING_BOLD, Theme.WARNING ) + Theme.RESET, stream = EStream.SYSTEM )
                    MCMD.print( Theme.WARNING + "---------------------------------------------------------" + Theme.RESET, stream = EStream.SYSTEM )
                    common_commands.start_ui( ERunMode.CLI )
    
    except UserExitError as ex:
        MCMD.print( "[{}]".format( ex ), stream = EStream.SYSTEM )
    finally:
        MCMD.print( "{} script executor has exited.".format( "ARGV" if read_argv else "CLI" ), stream = EStream.SYSTEM )
        
        if not queue:
            __save_history_function()


class IntermakePrompt:
    
    
    def __repr__( self ):
        host = MENV.host
        if isinstance( host, ConsoleHost ):
            if host.console_settings.hide_streams:
                prefix = ""
            else:
                prefix = ">>> "
            
            return prefix + str( MENV.host.browser_path ) + ">"
        else:
            return "$" + str( host ) + "$"


INTERMAKE_PROMPT = IntermakePrompt()


def __read_arg():
    print( Theme.PROMPT, end = "", file = sys.stderr )
    prompt = str( INTERMAKE_PROMPT )
    
    try:
        if file_helper.is_windows():
            print( prompt, end = "", file = sys.stderr )
            return input()
        else:
            return input( prompt )
    except EOFError:
        raise UserExitError( "End of standard input" )
    except KeyboardInterrupt:
        raise UserExitError( "Keyboard quit" )
    finally:
        print( Theme.RESET, end = "", file = sys.stderr )
        sys.stdout.flush()


def execute_text( x ) -> None:
    if x.startswith( "#" ):
        return
    
    # Environment variable replacement
    for k, v in os.environ.items():
        x = x.replace( "$(" + k + ")", v )
    
    # Alias replacement
    stn, cfg = get_clf_settings()
    
    for k, v in stn.aliases.items():
        x = x.replace( k, v )
    
    for k, v in cfg.aliases.items():
        x = x.replace( k, v )
    
    if x.startswith( "?" ) or x.endswith( "?" ):
        x = x.strip( "?" )
        x = x.strip()
        
        user_commands = shlex.split( x )
        cmds = ["help"]
        
        if len( user_commands ) >= 1:
            cmds += [user_commands[0]]
        
        if len( user_commands ) >= 2:
            cmds += [user_commands[-1]]
    else:
        try:
            cmds = shlex.split( x )
        except Exception as ex:
            raise SyntaxError( "Not processing «{}» because it isn't valid command string.".format( x ) ) from ex
    
    __execute_command( cmds )
