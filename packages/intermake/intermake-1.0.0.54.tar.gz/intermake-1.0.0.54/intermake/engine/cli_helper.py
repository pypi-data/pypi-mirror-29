"""
Helper functions for CLI-based plugins.
"""

from enum import Enum
from typing import List, Optional, Union

# noinspection PyPackageRequirements
from flags import Flags

from intermake.engine import constants
from intermake.engine.environment import MCMD, MENV
from intermake.engine.plugin import Plugin
from intermake.engine.theme import Theme
from intermake.hosts.base import PluginHost
from mhelper import ansi, ansi_format_helper, ansi_helper, string_helper, markdown_helper


__print_banner_displayed = False


def get_details_text( plugin: Plugin ) -> str:
    """
    Gets the help text of the specified plugin, formatted for display in the CLI and returned as a single string.
    """
    result = []
    get_details( result, plugin )
    return "\n".join( result )


def get_details( result: List[str], plugin: Plugin, show_quick: bool = False ) -> None:
    """
    Gets the help text of the specified plugin, formatted for display in the CLI and returned as a list of lines.
    """
    type_ = ""  # plugin.get_plugin_type()
    
    type_colour = Theme.BOX_TITLE_RIGHT
    bar_colour = Theme.BORDER
    deco_colour = type_colour
    
    name = MENV.host.translate_name( plugin.name )  # type:str
    
    if not plugin.is_visible:
        name_colour_extra = Theme.SYSTEM_NAME
    elif plugin.is_highlighted:
        name_colour_extra = Theme.CORE_NAME
    else:
        name_colour_extra = Theme.COMMAND_NAME
    
    env = MENV
    line_width = env.host.console_width
    
    result_b = []
    
    if show_quick:
        name = name.ljust( 20 )
        prefix = Theme.BORDER + "::" + Theme.RESET
        
        result_b.append( prefix + " " + type_colour + type_ + Theme.RESET + " " + name_colour_extra + name + Theme.RESET + " -" )
        
        line = plugin.get_description().strip()
        line = env.host.substitute_text( line )
        
        line = line.split( "\n", 1 )[0]
        
        line = string_helper.fix_width( line, line_width - len( name ) - 10 )
        
        line = highlight_keywords( line, plugin, Theme.COMMAND_NAME, Theme.COMMENT )
        
        result_b.append( " " + Theme.COMMENT + line + Theme.RESET + " " + prefix )
        
        result.append( "".join( result_b ) )
        
        return
    
    DESC_INDENT = 4
    
    ARG_INDENT = 8
    ARG_DESC_INDENT = 30
    
    DESC_INDENT_TEXT = " " * DESC_INDENT
    
    result.append( "  "
                   + bar_colour + "_"
                   + name_colour_extra + name
                   + bar_colour + "_" * (line_width - len( name ) - len( type_ ) - 4)
                   + deco_colour
                   + type_colour + type_
                   + Theme.RESET )
    
    result.append( Theme.COMMENT + "  Aliases: " + ", ".join( x for x in plugin.names if x != name ) + Theme.RESET )
    
    #
    # DESCRIPTION
    #
    desc = plugin.get_description()
    desc = format_doc( desc )
    
    for line in ansi_helper.wrap( desc, line_width - DESC_INDENT ):
        result.append( DESC_INDENT_TEXT + line + Theme.RESET )
    
    #
    # ARGUMENTS
    #
    extra = False
    
    for i, arg in enumerate( plugin.args ):
        desc = arg.description or (str( arg.annotation ) + (" (default = " + str( arg.default ) + ")" if arg.default is not None else ""))
        desc = format_doc( desc, width = -1 )
        
        t = arg.annotation
        
        viable_subclass_type = t.get_indirectly_below( Enum ) or t.get_indirectly_below( Flags )
        
        if viable_subclass_type is not None:
            desc += Theme.RESET
            
            for k in viable_subclass_type.__dict__.keys():
                if not k.startswith( "_" ):
                    desc += "\n" + Theme.ENUMERATION + " * " + Theme.COMMAND_NAME + k + Theme.RESET
            
            desc += Theme.RESET
            
            if not extra:
                extra = arg.name
        
        blb = ansi.FORE_BRIGHT_CYAN
        
        arg_name = Theme.ARGUMENT_NAME + blb + MENV.host.translate_name( arg.name ) + "\n"
        
        default_text = str( arg.default ) if arg.default is not None else ""
        
        arg_name += "  " + Theme.COMMENT + blb + default_text
        
        desc += "\n"
        
        result.append( ansi_format_helper.format_two_columns( left_margin = ARG_INDENT,
                                                              centre_margin = ARG_DESC_INDENT,
                                                              right_margin = line_width,
                                                              left_text = arg_name,
                                                              right_text = desc,
                                                              left_prefix = Theme.ARGUMENT_NAME + blb,
                                                              left_suffix = ansi.RESET ) )
    
    if extra:
        result.append( "" )
        result.append( "    " + Theme.ENUMERATION + "*" + Theme.RESET +
                       " Specify the argument when you call " + Theme.COMMAND_NAME + "help" +
                       Theme.RESET + " to obtain the full details for these values. E.g. “" +
                       Theme.COMMAND_NAME + "help " + plugin.display_name + " " + extra + Theme.RESET + "”." )
        result.append( "" )


def format_doc( doc: str, width: int = 0 ) -> str:
    """
    Formats markdown.
    
    :param doc:        Restructured text.
    :param width:      Width of text, otherwise the console width will be used.
    :return:           Formatted text.
    """
    if doc is None:
        doc = ""
    
    doc = doc.strip()
    doc = MENV.host.substitute_text( doc )
    doc = markdown_helper.markdown_to_ansi( doc, width = width or MENV.host.console_width )
    doc = string_helper.highlight_quotes( doc, "«", "»", Theme.EMPHASIS, Theme.RESET )
    doc = string_helper.highlight_quotes( doc, '"', '"', '«' + Theme.EMPHASIS, Theme.RESET + '»' )
    return doc.strip()


def highlight_keywords( desc: Union[str, bytes], plugin_or_list, highlight = None, normal = None ):
    """
    Highlights the keywords in a plugin's description.
    :param desc:        Source string 
    :param plugin_or_list:      Either a plugin to get the keywords from, or a list of keywords.
    :param highlight:   Highlight colour 
    :param normal:      Normal colour 
    :return:            Modified string 
    """
    if highlight is None:
        highlight = Theme.ARGUMENT_NAME
    
    if normal is None:
        normal = Theme.RESET
    
    from intermake.engine.plugin import Plugin
    if isinstance( plugin_or_list, Plugin ):
        args = (z.name for z in plugin_or_list.args)
    else:
        args = plugin_or_list
    
    for arg in args:
        desc = desc.replace( "`" + arg + "`", highlight + arg + normal )
    
    return desc


def format_kv( key: str, value: Optional[object], spacer = "=" ):
    """
    Prints a bullet-pointed key-value pair to STDOUT
    """
    return "* " + Theme.COMMAND_NAME + key + Theme.BORDER + " " + "." * (39 - len( key )) + Theme.RESET + " " + spacer + " " + Theme.VALUE + str( value ) + Theme.RESET


def print_value( value: str ):
    """
    Prints a bullet-pointed value pair to STDOUT
    """
    MCMD.print( "* " + Theme.COMMAND_NAME + value + Theme.RESET )


def format_title( title: str ) -> str:
    return Theme.TITLE + string_helper.cjust( " " + str( title ) + " ", 20, "-" ) + Theme.RESET


def format_banner( subtitle: str, help_cmd: Optional[str], help_lst: Optional[str], full: bool = False ) -> str:
    """
    Formats a standard welcome message.
    
    :param subtitle:     The launch type / subtitle of the application. Leave blank for no subtitle. 
    :param help_cmd:     If the full banner is displayed, the command the user may invoke for help. Leave blank for no help. If `help_lst` is set, this must be set also. 
    :param help_lst:     If the full banner is displayed, the command the user may invoke to get the list of commands. Leave blank for no help. If `help_cmd` is set, this must be set also.
    :param full:         If not none, force the display of the full banner (true) or partial banner (false), otherwise host.host_settings.welcome_message will be honoured.
    :return:             The formatted welcome message is returned.
    """
    
    global __print_banner_displayed
    
    host = MENV.host  # type: PluginHost
    
    if full is None:
        full = host.host_settings.welcome_message
    
    if not full:
        return MENV.name + " " + MENV.version + ((" " + subtitle) if subtitle else "")
    
    r = []
    
    width = min( host.console_width, 100 )
    box_width = width - 3
    
    BOX_END = Theme.BANNER_END_OF_THE_LINE + "▖" + Theme.RESET
    help = Theme.BANNER_MAIN + MENV.name + (("/" + subtitle) if subtitle else "") + ". "
    if help_cmd and help_lst:
        help += "Use " + Theme.BANNER_COMMAND_NAME + help_cmd + Theme.BANNER_MAIN + " for help and " + Theme.BANNER_COMMAND_NAME + help_lst + Theme.BANNER_MAIN + " to view commands."
    help = ansi_helper.ljust( help, width, " " ) + Theme.RESET
    
    prefix = constants.INFOLINE_SYSTEM
    prefix_s = constants.INFOLINE_SYSTEM_CONTINUED
    
    if not __print_banner_displayed:
        r.append( prefix + Theme.BANNER_ZERO + "█" * box_width + BOX_END )
        r.append( prefix_s + Theme.BANNER_ZERO + "██" + string_helper.centre_align( " {} ".format( MENV.name.upper() ), box_width - len( MENV.version ) - 2, "█", prefix = Theme.BANNER_REVERSED, suffix = Theme.BANNER_ZERO ) + Theme.BANNER_REVERSED + " " + MENV.version + " " + Theme.BANNER_ZERO + "█" + BOX_END )
        r.append( prefix_s + Theme.BANNER_ZERO + "█" * box_width + "██" + BOX_END )
    
    else:
        r.append( prefix_s + Theme.BANNER_MAIN + " " * box_width + "   " + Theme.RESET )
    
    if help_cmd:
        r.append( prefix_s + help )
    
    if not __print_banner_displayed:
        r.append( prefix_s + Theme.BANNER_MAIN + ("The current workspace is '" + MENV.local_data.get_workspace() + "'").ljust( width ) + Theme.RESET )
        
        if MENV.version.startswith( "0." ):
            r.append( prefix_s + Theme.BANNER_MAIN + "This application is in development; not all features may work correctly and the API may change.".ljust( width ) + Theme.RESET )
    
    __print_banner_displayed = True
    
    return "\n".join( r )


def highlight_quotes( text ):
    text = string_helper.highlight_quotes( text, "`", "`", Theme.COMMAND_NAME, Theme.RESET )
    return text
