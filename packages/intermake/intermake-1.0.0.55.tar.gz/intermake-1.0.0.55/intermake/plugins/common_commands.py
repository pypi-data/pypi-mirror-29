"""
This module holds the Intermake common command set.

All functions here are decorated with `@command`, which allows them to be passed as command line arguments to the application.
See `@command` for more details.
"""

import os
import sys
from typing import Iterable, Optional, cast, List
from os import path

from intermake.hosts.frontends.command_line import _CommandLineFrontendSettings
from mhelper import NotSupportedError, ansi_format_helper, array_helper, string_helper, io_helper, MOptional, Filename, EFileMode, LOGGERS, file_helper
from intermake.engine import cli_helper, function_inspector
from intermake.engine.async_result import AsyncResult
from intermake.engine.environment import MCMD, MENV
from intermake.engine.mandate import PluginArg
from intermake.engine.plugin import Plugin
from intermake.engine.plugin_manager import PluginFolder
from intermake.engine.theme import Theme
from intermake.hosts.base import ERunMode, RunHostArgs, ERunStatus
from intermake.hosts.console import ConsoleHost, UserExitError
from intermake.hosts.frontends import command_line
from intermake.plugins import visibilities
from intermake.plugins.command_plugin import command, help_command
from intermake.plugins.setter_plugin import SetterPlugin


__mcmd_folder_name__ = "system"


@command( names = ["exit", "x", "quit", "q", "bye"], visibility = visibilities.CLI, highlight = True )
def cmd_exit( force: bool = False ) -> None:
    """
    Exits the program safely.
    Note that pressing `CTRL+C` in the CLI will also exit the program safely.
    If a command is running, then `CTRL+C` will stop that command and return you to the CLI.
    
    :param force: Force-quits the program. Don't do this unless you can't quit any other way, modified data and command history will not be saved. 
    """
    if force:
        sys.exit( 1 )
    else:
        raise UserExitError( "User requested exit" )


@command( visibility = visibilities.CLUSTER )
def compute_cluster( index: Optional[int] = None,
                     number: Optional[int] = None,
                     single: bool = False,
                     detect: bool = False,
                     ignore_errors: bool = False ) -> None:
    """
    For compute clusters, sets the index of the current processes, and the number of processes.
    
    The number of processes is used to calculate how a workload is divided.
    The index of the current processor is used to obtain which portion of the workload to perform.
    
    Note that this is only meaningful with plugins that actually support multi-threaded/multi-processed operations.
    See the details on individual plugins for more details.
    
    If no changes are specified the current status is simply reported.
    
    If you are not operating in a multi-process environment, using this feature may result in only partial workloads being completed.
    
    This feature only works for the CLI version.
    The GUI version defaults to multi-threaded behaviour instead, which can be configured through the settings screen or the {set} command. 
     
    :param ignore_errors: Ignores errors if this is not a compute cluster and `detect` is set.
    :param single:        Bypasses the check that ensures that `number` is not `1`. Used only if you accidentally set multi-processing on a single-processor system and wish to turn it off again. 
    :param detect:        Read from system. Currently only supports "sge".
    :param index:         Zero-based index of this process
    :param number:        Number of processes, and so the last index is `number - 1`.
    
    :exception NotSupportedError: Raised when the `detect` flag is set but the system has been identified as having no multiprocess support
    """
    host = MCMD.host
    
    if not isinstance( host, ConsoleHost ):
        raise ValueError( "Bad use of 'cli_multi_processing' command outside CLI. Only the CLI supports compute clusters; the GUI uses its own internal threading and is not suited to computer cluster use." )
    
    if detect:
        if index is not None or number is not None or single:
            raise ValueError(
                    "Ambiguous command: `auto` specified but `index`, `number` and/or `single` have also been specified." )
        
        if "SGE_TASK_ID" in os.environ and "SGE_TASK_LAST" in os.environ:
            MCMD.information( "System identified as SGE." )
            
            index = int( os.environ["SGE_TASK_ID"] ) - 1
            number = int( os.environ["SGE_TASK_LAST"] )
        elif ignore_errors:
            MCMD.warning(
                    "`cli_multi_processing` has been called with the `detect` flag set but the system has been identified as having no multiprocess support." )
            index = 0
            number = 1
            single = True
        else:
            raise NotSupportedError(
                    "`cli_multi_processing` has been called with the `detect` flag set but the system has been identified as having no multiprocess support." )
    
    if index is not None:
        if number is None:
            raise ValueError( "If the `index` argument is provided the `number` argument must also be specified." )
        
        if not single:
            if number == 1:
                raise ValueError(
                        "Attempting to set `number` to `1` indicates this is not multiprocessing. If you are trying to turn multi-processing off, set the `single` parameter to `True`." )
        
        if number < 0:
            raise ValueError( "Invalid `number` parameter: {}.".format( number ) )
        
        if index < 0 or index >= number:
            raise ValueError(
                    "Invalid `index` parameter: {}. Index must be in the range 0 to {} (inclusive), when `number` = {}.".format(
                            index, number - 1, number ) )
        
        host.set_config_multi_processing( int( index ), int( number ) )
        MCMD.print( "Value changed." )
    
    my_index, array_count = host.get_config_multi_processing()
    
    MCMD.print( "Host is operating as process {0} of a {1} process array.".format( my_index, array_count ) )


@command( names = ["error", "err", "print_error"], visibility = visibilities.CLI & visibilities.ADVANCED )
def error() -> None:
    """
    Displays the details of the last error encountered.
    """
    MCMD.print( "LAST ERROR:" )
    host = MCMD.host
    result = host.last_error  # type: AsyncResult
    
    if result.exception is not None:
        MCMD.print( ansi_format_helper.format_traceback( result.exception, result.traceback ) )
    else:
        MCMD.print( "There is no error." )


@command( names = ["use", "set_visibility"], visibility = visibilities.COMMON )
def use( category: Optional[str] = None, all: bool = False ) -> None:
    """
    Shows or hides command sets.

    :param all:      When listing the available modes, setting this flag shows all classes, even if they appear to be non-functional.
    :param category: Mode to show or hide. Leave blank to list the available modes. If this is an asterisk (`*`) then all modes are set to visible.
    """
    visibilities = MENV.plugins.find_visibilities()
    
    for visibility in visibilities:
        if category == "*":
            visibility.user_override = True
            MCMD.print( Theme.STATUS_YES + "{} is now shown ".format( visibility.name ) + Theme.RESET )
        elif visibility.name == category:
            if visibility.user_override is True:
                visibility.user_override = False
                MCMD.print( Theme.STATUS_NO + "{} is now hidden ".format( visibility.name ) + Theme.RESET )
                return
            elif visibility.user_override is False:
                visibility.user_override = None
                MCMD.print( Theme.STATUS_INTERMEDIATE + "{} has been reset to its default ({})".format( visibility.name, "shown" if visibility.is_visible else "hidden" ) + Theme.RESET )
                return
            else:
                visibility.user_override = True
                MCMD.print( Theme.STATUS_YES + "{} is now shown ".format( visibility.name ) + Theme.RESET )
                return
    
    for visibility in sorted( visibilities, key = lambda x: x.name ):
        if not visibility.is_functional and not all and category != "*":
            continue
        
        shown = visibility()
        MCMD.print( "{}{}{}{} {}".format( (Theme.STATUS_IS_NOT_SET if visibility.user_override is None else Theme.STATUS_IS_SET),
                                          "[X]" if shown else "[ ]",
                                          (Theme.STATUS_YES if shown else Theme.STATUS_NO) + " " + visibility.name.ljust( 20 ),
                                          Theme.RESET,
                                          visibility.comment ) )


@command( names = ["cmdlist", "cl", "commands"], visibility = visibilities.CLI, highlight = True )
def cmdlist( filter: Optional[str] = None, details: bool = False, all: bool = False ) -> None:
    """
     Lists the available commands

     Commands are listed as:

     «command_name» «command_type» «description»

     «command_name»: The name of the command. Use `help` to see the full path.
     «command_type»: The type of command, 
     «description» :  Command documentation. Use `help` to see it all.

     :param details: When `True`, full details are printed 
     :param all: When `True`, all commands are shown, regardless of their visibility.

     :param filter: Specify a category, folder, or filter results by text

     """
    # Get the list
    plugins: List[Plugin] = list( MENV.plugins.all_plugins() )
    
    # Filter the list
    if filter:
        filter_text = MCMD.host.translate_name( filter )
        
        # By category?
        filter_category = string_helper.find( source = MENV.plugins.find_visibilities(), search = filter_text, namer = MCMD.host.translate_name, fuzzy = False, default = None )
        
        if filter_category:
            plugins = [λplugin for λplugin in plugins if filter_category in λplugin.visibility_class]
        else:
            # By folder?
            filter_folder = string_helper.find( source = (x for x in MENV.plugins.plugins_root if x is PluginFolder), search = filter_text, namer = MCMD.host.translate_name, fuzzy = False, default = None )
            
            if filter_folder:
                plugins = [λplugin for λplugin in plugins if λplugin.parent is filter_folder]
            else:
                # By text?
                plugins = [λplugin for λplugin in plugins if filter_text in MCMD.host.translate_name( λplugin.name )]
        
        if not plugins:
            MCMD.print( "No plugins match your search term «{}».".format( filter ) )
            return
    
    # Sort the list
    plugins = sorted( plugins, key = lambda λplugin: ((MCMD.host.translate_name( λplugin.parent ) + ".") if λplugin.parent else "") + MCMD.host.translate_name( λplugin ) )
    
    # Print the results
    result = []
    last_parent = ""
    WIDTH = MCMD.host.console_width
    PREFIX = Theme.BORDER + "::" + " " * (WIDTH - 4) + "::" + Theme.RESET
    
    for plugin in plugins:
        if not (plugin.is_visible or all):
            continue
        
        parent = MCMD.host.translate_name( plugin.parent.name ) if plugin.parent else ""
        
        if parent != last_parent:
            padding_size = (WIDTH - len( parent )) // 2 - 1
            padding_text = Theme.BORDER + (":" * padding_size)
            
            if (len( parent ) % 2) != 0:
                padding_extra = ":"
            else:
                padding_extra = ""
            
            if result:
                result.append( PREFIX )
            
            result.append( padding_text + " " + Theme.BOX_TITLE + parent + " " + padding_text + padding_extra + Theme.RESET + "\n" + PREFIX )
            last_parent = parent
        
        cli_helper.get_details( result, plugin, not details )
    
    result.append( PREFIX )
    result.append( Theme.BORDER + ":" * WIDTH + Theme.RESET )
    
    MCMD.print( "\n".join( result ) )


@command( names = ["eggs", "example"], visibility = visibilities.ADVANCED )
def eggs( name: str = "no name", good: bool = False, repeat: int = 1 ) -> None:
    """
    Egg-sample command :)
    Prints a message.
     
    :param name:    Name of your egg-sample 
    :param good:    Is this a good egg-sample?
    :param repeat:  Number of times to repeat the egg-sample.
    """
    for _ in range( repeat ):
        MCMD.print( "This is an example command. «{}» is a {} egg-sample.".format( name, "GOOD" if good else "BAD" ) )


@command( visibility = visibilities.ADVANCED )
def python_help( thing: object = None ) -> None:
    """
    Shows Python's own help.

    :param thing: Thing to show help for, leave blank for general help.
    """
    import pydoc
    
    if thing is None:
        pydoc.help()
    else:
        pydoc.help( thing )


@help_command()
def basic_help() -> str:
    """
    Basics help point.
    """
    return MENV.host.substitute_text( string_helper.fix_indents( MENV.host.get_help_message() ) ) + "\n\n" + topics_help()


@command( visibility = visibilities.ADVANCED )
def history( find: str = "" ):
    """
    Prints CLI history.
    :param find:    If specified, only lists lines containing this text
    """
    from intermake.hosts.frontends.command_line import iter_history
    for line in iter_history():
        if find in line:
            MCMD.print( line )


def topics_help() -> str:
    """
    Shows the list of help topics.
    """
    topics = []
    
    for plugin in MENV.plugins:
        if plugin.visibility_class is visibilities.HELP:
            topics.append( plugin )
    
    r = []
    
    r.append( Theme.TITLE + "-------------------- {} HELP TOPICS --------------------".format( len( topics ) ) + Theme.RESET )
    r.append( "Use one of the following commands for more help on specific topics:" )
    
    for plugin in topics:
        r.append( Theme.COMMAND_NAME + MENV.host.translate_name( plugin.name ) + Theme.RESET )
    
    return "\n".join( r )


in_help = False


@command( highlight = True, names = ["help", "mcmd_help", "mhelp", "h"] )
def cmd_help( command_name: Optional[str] = None, argument_name: Optional[str] = None ) -> None:
    """
    Shows help 
    :param command_name: Name of command or script to get help for. If not specified then general help is given. 
    :param argument_name: Name of the argument to get help for. If not specified then help for the command is given.
    :return: 
    """
    if not command_name:
        basic_help()
        return
    else:
        command = command_line.find_command( command_name )
    
    if command is None:
        return
    
    if not argument_name:
        MCMD.print( cli_helper.get_details_text( command ) )
    else:
        argument = string_helper.find(
                source = command.args,
                namer = lambda x: MCMD.host.translate_name( x.name ),
                search = argument_name,
                detail = "argument" )  # type: PluginArg
        
        t = argument.annotation.get_indirectly_below( object )
        
        if t is None:
            raise ValueError( "Cannot obtain type above object from «{}».".format( argument.annotation ) )
        
        console_width = MENV.host.console_width
        
        MCMD.print( ansi_format_helper.format_two_columns( left_margin = 4, centre_margin = 30, right_margin = console_width, left_text = Theme.FIELD_NAME + "name       " + Theme.RESET, right_text = Theme.ARGUMENT_NAME + argument.name + Theme.RESET ) )
        MCMD.print( ansi_format_helper.format_two_columns( left_margin = 4, centre_margin = 30, right_margin = console_width, left_text = Theme.FIELD_NAME + "type name  " + Theme.RESET, right_text = t.__name__ ) )
        MCMD.print( ansi_format_helper.format_two_columns( left_margin = 4, centre_margin = 30, right_margin = console_width, left_text = Theme.FIELD_NAME + "optional   " + Theme.RESET, right_text = str( argument.can_be_none ) ) )
        MCMD.print( ansi_format_helper.format_two_columns( left_margin = 4, centre_margin = 30, right_margin = console_width, left_text = Theme.FIELD_NAME + "default    " + Theme.RESET, right_text = Theme.COMMAND_NAME + str( argument.default ) + Theme.RESET ) )
        MCMD.print( ansi_format_helper.format_two_columns( left_margin = 4, centre_margin = 30, right_margin = console_width, left_text = Theme.FIELD_NAME + "description" + Theme.RESET, right_text = cli_helper.highlight_keywords( argument.description, command ) ) )
        
        # Type docs
        docs = function_inspector.extract_documentation( t.__doc__, "data" )
        MCMD.print( ansi_format_helper.format_two_columns( left_margin = 4, centre_margin = 30, right_margin = console_width, left_text = Theme.FIELD_NAME + "type       " + Theme.RESET, right_text = docs[""] or "Values:" ) )
        
        for key, value in docs.items():
            if key and value:
                MCMD.print( ansi_format_helper.format_two_columns( left_margin = 34, centre_margin = 50, right_margin = console_width, left_text = Theme.ENUMERATION + key + Theme.RESET, right_text = value ) )


@command( visibility = visibilities.ADVANCED[visibilities.CLI] )
def version( stdout: bool = False ) -> None:
    """
    Shows the application version.
    
    :param stdout: Print to std.out.
    """
    if stdout:
        print( MENV.version )
    else:
        MCMD.print( "VERSION:" )
        name = MENV.name
        version = MENV.version
        MCMD.print( name + " " + version )


@command( names = ["system"], visibility = visibilities.ADVANCED )
def system( command_: str ) -> None:
    """
    Invokes a system command in the current terminal.
    
    :param command_: Command to execute.
    """
    os.system( command_ )


@command( names = ["eval"], visibility = visibilities.ADVANCED )
def cmd_eval( command_: str ) -> None:
    """
    Evaluates a Python statement and prints the result.
    
    :param command_: Python statement to run
    """
    MCMD.print( str( eval( command_ ) ) )


@command( names = ["cls", "clear"], visibility = visibilities.ADVANCED )
def cls() -> None:
    """
    Clears the CLI.
    """
    # The proper way is to send the correct ANSI sequence, however in practice this produces odd results.
    # So we just use the specific system commands.
    if sys.platform.lower() == "windows":
        system( "cls" )
    else:
        system( "clear ; clear" )  # once doesn't clear the terminal properly


@command( visibility = visibilities.ADVANCED )
def start_cli() -> None:
    """
    Starts the UI: Command line interface
    
    See also :function:`prepare_cli`.
    """
    start_ui( ERunMode.CLI )


@command( names=["gui", "start_gui"], visibility = visibilities.ADVANCED )
def start_gui() -> None:
    """
    Starts the UI: Graphical user interface
    """
    start_ui( ERunMode.GUI )


@command( names=["pyi", "start_pyi"],visibility = visibilities.ADVANCED )
def start_pyi() -> None:
    """
    Starts the UI: Python interactive interface
    """
    start_ui( ERunMode.PYI )


@command( names = ["ui", "start_ui"], visibility = visibilities.ADVANCED )
def start_ui( mode: Optional[ERunMode] = None ) -> None:
    """
    Switches the user-interface mode.
    
    :param mode: Mode to use.
    """
    if mode is None:
        MCMD.print( "The current host is {}.".format( MCMD.host ) )
        return
    
    if mode in (ERunMode.PYS, ERunMode.JUP):
        MCMD.print( "The {} host does not possess its own frontend and cannot be started manually.".format( mode ) )
        return
    
    MENV.host.on_status_changed( ERunStatus.PAUSE )
    previous_host = MENV.host
    MENV.host = MENV.host_provider( mode )
    
    try:
        args = RunHostArgs()
        
        args.can_return = isinstance( previous_host, ConsoleHost ) and cast( ConsoleHost, previous_host ).console_configuration.run_mode != ERunMode.ARG
        
        MENV.host.on_status_changed( ERunStatus.RUN )
        if MENV.host.run_host( args ) is False:
            raise UserExitError( "Quit CLI selected in GUI" )
    except Exception as ex:
        raise ValueError( "Error running host «{}».".format( MENV.host ) ) from ex
    
    MENV.host.on_status_changed( ERunStatus.STOP )
    MENV.host = previous_host
    MENV.host.on_status_changed( ERunStatus.RESUME )


class LocalDataPlugin( Plugin ):
    """
    Modifies the local data store.
    
    Pass arguments to modify, or pass no arguments to view.
    
    :remarks:
    Invoking this plugin is not the best way to modify settings _programmatically_.
    Modify such settings via access to the actual `object`, and then call the associated save function to commit the changes to `MENV.local_data.store` (if the property is not bound). 
    """
    
    
    def __init__( self ) -> None:
        super().__init__( names = ["local"], description = str( self.__doc__ ), visibility = visibilities.ADVANCED )
        
        self.__arg_drop = PluginArg( "drop", Optional[str], None, "SPECIAL: When set to the name of a setting, deletes that setting. May require an application restart. All other parameters are ignored." )
        self.__arg_view = PluginArg( "view", Optional[str], None, "SPECIAL: When set to the name of a setting, views that setting. All other parameters are ignored." )
    
    
    @property
    def args( self ) -> Iterable[PluginArg]:
        store = MENV.local_data.store
        
        keys = store.keys()
        
        args = []
        
        for key in keys:
            data_object = store[key]
            
            if type( data_object ) in (dict, list):
                continue
            
            for arg in SetterPlugin.extract_arguments( data_object, formatter = lambda x: key + "/" + x, defaults = MENV.host.is_gui ):
                arg.tag_key = key
                arg.tag_object = data_object
                args.append( arg )
        
        args.append( self.__arg_drop )
        args.append( self.__arg_view )
        
        return args
    
    
    def virtual_run( self ) -> Optional[object]:
        store = MENV.local_data.store
        modified_keys = set()
        
        r = []
        
        drop = self.__arg_drop.get_value()
        view = self.__arg_view.get_value()
        
        if drop:
            del store[drop]
            return
        
        if view:
            MCMD.information( str( view ) )
            MCMD.information( store[view] )
            return
        
        for arg_value in MCMD.args:
            if arg_value.value is None:
                continue
            
            arg = arg_value.arg
            
            if not hasattr( arg, "tag_object" ):
                continue
            
            data_object = arg.tag_object
            target_field = arg.tag_field_name
            target_key = arg.tag_key
            
            data_object.__dict__[target_field] = arg_value.value
            
            modified_keys.add( target_key )
            
            r.append( cli_helper.format_kv( arg_value.name, data_object.__dict__[target_field], "->" ) )
        
        if modified_keys:
            for modified_key in modified_keys:
                store.commit( modified_key )
        else:
            for arg_value in MCMD.args:
                arg = arg_value.arg
                
                if not hasattr( arg, "tag_object" ):
                    continue
                
                data_object = arg.tag_object
                target_field = arg.tag_field_name
                
                text = data_object.__dict__[target_field]
                
                if isinstance( text, list ) or isinstance( text, tuple ) or isinstance( text, set ):
                    text = "List of {} items".format( len( text ) )
                else:
                    text = str( text )
                
                if len( text ) > 40:
                    text = text[:40] + "..."
                
                r.append( cli_helper.format_kv( arg_value.name, text, ":" ) )
        
        MCMD.information( "\n".join( r ) )


LOCAL_DATA_PLUGIN = LocalDataPlugin()
MENV.plugins.register( LOCAL_DATA_PLUGIN )


@command( visibility = visibilities.ADVANCED )
def workspace( directory: Optional[str] = None ) -> None:
    """
    Gets or sets the $(APP_NAME) workspace (where settings and caches are kept)
     
    :param directory:   Directory to change workspace to. This will be created if it doesn't exist. The workspace will take effect from the next $(APP_NAME) restart. 
    """
    MCMD.information( "WORKSPACE: " + MENV.local_data.get_workspace() )
    
    if directory:
        MENV.local_data.set_redirect( directory )
        MCMD.information( "Workspace will be changed to «{}» on next restart.".format( directory ) )


@command( names = ["import", "python_import"], visibility = visibilities.ADVANCED )
def import_( name: str ) -> None:
    """
    Wraps the python `import` command, allowing external sets of plugins to be imported.
    
    :param name: Name of the package to import. 
    """
    old_count = array_helper.count( MENV.plugins.all_plugins() )
    orig_namespace = MENV.plugins.namespace
    MENV.plugins.namespace = name
    __import__( name )
    new_count = array_helper.count( MENV.plugins.all_plugins() )
    
    MCMD.print( "Import {} OK.".format( name ) )
    
    if old_count != new_count:
        MCMD.print( "{} new plugins.".format( new_count - old_count ) )
    
    MENV.plugins.namespace = orig_namespace


@command( names = ["autostore_warnings"], visibility = visibilities.ADVANCED )
def cmd_autostore_warnings() -> None:
    """
    Displays, in more detail, any warnings from the autostore.
    """
    from intermake.datastore.local_data import autostore_warnings
    
    if len( autostore_warnings ) == 0:
        MCMD.information( "No warnings." )
    
    for i, message in enumerate( autostore_warnings ):
        MCMD.information( Theme.TITLE + "WARNING {} OF {}".format( i, len( autostore_warnings ) ) + Theme.RESET )
        MCMD.information( message )


@command( visibility = visibilities.ADVANCED )
def messages( file: MOptional[Filename[EFileMode.WRITE]] = None ) -> None:
    """
    Repeats the last output messages.
    
    :param file:    See `file_write_help`.
    """
    index, last_result = MENV.host.last_results[-1]
    
    
    def ___print( x ):
        if x.endswith( "\n" ):
            x = x[:-1]
        
        MCMD.print( x )
    
    
    with io_helper.open_write( file ) as file_out:
        for message in last_result.messages:
            file_out.write( message + "\n" )


@command( visibility = visibilities.ADVANCED )
def make_boring( boring: bool = True ) -> None:
    """
    Disables colour, unicode and stream output.
    Added this after people complained about the exciting default colour scheme.
    
    :param boring:  Boring status.
    """
    host = MENV.host
    
    if not isinstance( host, ConsoleHost ):
        return
    
    host.console_settings.remove_utf = boring
    host.console_settings.remove_ansi = boring
    host.console_settings.hide_streams = boring
    
    MCMD.progress( "CONSOLE SETTINGS" )
    MCMD.progress( "NON-ASCII [{0}], ANSI-COLOURS [{0}], SIDEBAR [{0}]".format( "OFF" if boring else "ON" ) )


@command( visibility = visibilities.ADVANCED )
def log( name: Optional[str] = None ) -> None:
    """
    Enables, disables, or displays loggers.
    
    :param name:    Logger to enable or disable, or `None` to list all.
    """
    for logger in LOGGERS:
        if name == logger.name:
            if logger.enabled is False:
                logger.enabled = True
            elif logger.enabled is True:
                logger.enabled = False
            else:
                MCMD.print( "Cannot change status because this logger has been bound to another destination." )
        
        MCMD.print( cli_helper.format_kv( logger.name, logger.enabled ) )


@command( names = ["setwd", "chdir"], visibility = visibilities.ADVANCED )
def setwd( path: Optional[str] = None ) -> None:
    """
    Displays or sets the working directory.
    This is not the same as the `cd` command, which navigates $(APPNAME)'s virtual object hirarchy.
    
    :param path:    Path to set.
    """
    if path:
        os.chdir( path )
    
    MCMD.print( os.getcwd() )


__EXT_IMK = ".imk"


@command( visibility = visibilities.ADVANCED )
def source( file_name: Filename[EFileMode.READ, __EXT_IMK] ) -> None:
    """
    Executes a file using the command line interpreter.
    This can be better than pipeing to std-in, since, with `source`, the CLI will halt if it encounters an error rather than continuing with future commands. 
    
    :param file_name:   File to execute. If this cannot be found the `.imk` extension will be attempted. 
    """
    if not path.isfile( file_name ):
        file_name += ".imk"
    
    if not path.isfile( file_name ):
        raise ValueError( "The path «{}» cannot be found or is not a file.".format( file_name ) )
    
    for line in file_helper.read_all_lines( file_name ):
        command_line.execute_text( line )


@help_command()
def format_help() -> None:
    """
    Displays help on formatting items
    """
    import stringcoercion
    r = []
    
    for coercer in stringcoercion.get_default_coercer().coercers:
        if coercer.__doc__:
            r.append( "* " + coercer.__doc__.strip() )
    
    MCMD.print( cli_helper.format_doc( "\n".join( r ) ) )


@command( names = ["cli", "prepare_cli"] )
def prepare_cli( store: bool = False ) -> None:
    """
    When called, ensures that the CLI is invoked:
        * When an error occurs in ARG mode
        * When ARG mode completes
    
    :remarks:
    This is an alternative to putting `CLI` at the end of the command string, becuase it ensures that even in error, the CLI is started.
    
    :param store:   Settings are saved to disk (they can be reverted through the :method:`local`). 
    """
    s: _CommandLineFrontendSettings = command_line.get_clf_settings()[0 if store else 1]
    s.error_invokes_cli = True
    s.args_invokes_cli = True


@command( visibility = visibilities.ADVANCED )
def alias( target: Optional[str] = None, source: Optional[str] = None, store: bool = False ) -> None:
    """
    Creates or displays a command line alias.
    Aliases are replaced verbatim, so if you create an alias `"e" --> "xyz"` then `hello` will be interpreted as `hxyzllo`.
    
    :param store:   When true, displays or modifies the permanent list
                    When false, displays or modifies the list for this session 
    :param target:  Term to find. If None prints all aliases.
    :param source:  New text. If None displays the alias. If empty deletes the alias. 
    """
    
    s = command_line.get_clf_settings()[0 if store else 1]
    
    if target is None:
        MCMD.print( "{} aliases.".format( len( s.aliases ) ) )
        for k, v in s.aliases.items():
            MCMD.print( cli_helper.format_kv( k, v ) )
        return
    
    if source is not None:
        if not source:
            del s.aliases[target]
        else:
            s.aliases[target] = source
        
        s.aliases = s.aliases  # commits to local data store 
    
    MCMD.print( cli_helper.format_kv( target, s.aliases.get( target ) ) )


@help_command()
def file_write_help():
    """
    Help on writing files.
    """
    return """
    Takes either:
        * A filename
        * `stdout` - writes to stdout
        * `null` - doesn't write anywhere
        * `clip` - writes to the clipboard
        * `` (default) - writes to the current UI
        """
