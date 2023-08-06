from typing import Optional

import sys

from intermake.plugins.setter_plugin import setter_command
from mhelper import string_helper, ansi
import stringcoercion

from intermake.engine.environment import MCMD, MENV
from intermake.hosts.frontends import command_line
from intermake.hosts.console import ConsoleHost, ConsoleHostConfiguration
from intermake.plugins.command_plugin import command
from intermake.plugins.visibilities import TEST
from intermake.engine import cli_helper


@command( visibility = TEST )
def console_width():
    """
    Prints the console width.
    """
    w = MCMD.host.console_width
    msg = "Console width hint is {}. This banner is the same size as the console width hint.".format( MCMD.host.console_width )
    msg = string_helper.max_width( msg, w - 4 )
    MCMD.print( "+" * w )
    MCMD.print( "+ " + msg + " " * (w - len( msg ) - 4) + " +" )
    MCMD.print( "+" * w )


@command( visibility = TEST )
def py_modules():
    """
    Lists the Python modules
    """
    for x in sys.modules.keys():
        cli_helper.print_value( x )


@command( visibility = TEST )
def test_progress( fast: bool = False ):
    """
    Does nothing.
    
    :param fast: Does nothing faster
    """
    count = 1000000 if fast else 10000000
    
    with MCMD.action( "Doing some work for you!", count ) as action:
        for n in range( count ):
            action.increment()


@command( visibility = TEST )
def test_progress_2():
    """
    Does nothing.
    """
    count = 10000000
    
    with MCMD.action( "Doing some work for you!" ) as action:
        for n in range( count ):
            action.still_alive()


@command( visibility = TEST )
def test_banner():
    """
    Tests the banner
    
    :param launch_type: Type to display banner for.
    """
    print( cli_helper.format_banner( "<value>", "<value>", "<value>", full = True ) )


@command( visibility = TEST )
def test_error():
    """
    Tests the error handling capabilities of the host
    """
    raise ValueError( "This is an error." )


@command( names = ["echo", "test_echo"], visibility = TEST )
def test_echo( text: str ):
    """
    Echos the text.
    :param text: Text to echo. Also accepts `on` and `off`, which turn command echoing on or off (temporarily, for the current session - use `local` to save settings for next session).
    """
    if text.lower() == "on":
        host = MENV.host
        if isinstance( host, ConsoleHost ):
            host.console_configuration.force_echo = True
        MCMD.print( "Echo is on" )
        return
    elif text.lower() == "off":
        host = MENV.host
        if isinstance( host, ConsoleHost ):
            host.console_configuration.force_echo = False
        MCMD.print( "Echo is off" )
        return
    
    MCMD.print( text )


@command( visibility = TEST )
def test_coercers():
    """
    Prints out the coercers in the stringcoercion library.
    """
    for coercer in stringcoercion.get_default_coercer().coercers:
        MCMD.print( str( coercer ) )


@command( visibility = TEST )
def test_modules( filter: Optional[str] = None ):
    """
    Prints out the loaded modules.
    :param filter:  Filter by name.
    """
    for module in sys.modules.values():
        if filter is not None and not filter.lower() in module.__name__.lower():
            continue
        
        MCMD.print( ansi.FORE_GREEN + module.__name__ + ansi.RESET )
        MCMD.print( ansi.FORE_WHITE + (module.__file__ if hasattr( module, "__file__" ) else "").rjust( MENV.host.console_width ) + ansi.RESET )


@setter_command( visibility = TEST )
def adv_set() -> ConsoleHostConfiguration:
    """
    Debugging command. Sets CLI parameters.
    """
    host = MENV.host
    
    if isinstance( host, ConsoleHost ):
        return host.console_configuration
    else:
        raise ValueError( "This operation only works for the Console Host." )


@command( visibility = TEST )
def get_intermake_css( css: Optional[str] = None ):
    """
    Gets the Intermake CSS.
    If pyperclip is installed, the result is copied to the clipboard, otherwise it is printed to stdout.
    
    :param css: Theme
    """
    from intermake.hosts.frontends.gui_qt import intermake_gui
    css = intermake_gui.default_style_sheet( css )
    
    try:
        import pyperclip
        pyperclip.copy( css )
        MCMD.print( "Copied to clipboard." )
    except ImportError:
        print( "css" )
        MCMD.print( "Printed to stdout (pyperclip not installed so not copied to clipboard)." )


@command( names = ["which", "what"], visibility = TEST )
def which( text: str ) -> None:
    """
    Finds which command will be matched if the user types "text".
    :param text: Text to find
    """
    
    fn = command_line.find_command( text )
    
    if fn:
        MCMD.information( cli_helper.format_kv( "Result", MCMD.host.translate_name( fn.name ) ) )
    else:
        MCMD.information( cli_helper.format_kv( "Result", "(no result)" ) )
