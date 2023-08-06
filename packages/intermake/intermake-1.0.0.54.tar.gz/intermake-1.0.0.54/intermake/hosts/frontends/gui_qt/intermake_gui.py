import warnings
from os import path
from typing import Set
from mhelper import file_helper
from intermake.engine.environment import MENV


def default_style_sheet( file_name = None ):
    """
    Gets the contents of the default style sheet.
    """
    host = MENV.host
    
    if not hasattr( host, "TAG_default_style_sheet" ) or host.TAG_default_style_sheet is None:
        if file_name is None:
            if MENV.host.is_gui:
                file_name = MENV.host.gui_settings.gui_css
            else:
                file_name = ""
        
        if "#" in file_name:
            file_name, section = file_name.split( "#", 1 )
        else:
            section = "default"
        
        if not file_name:
            file_name = "default.css"
        
        if not path.sep in file_name:
            if "." not in file_name:
                file_name += ".css"
            
            file_name = path.join( file_helper.get_directory( __file__ ), file_name )
        
        if not path.isfile( file_name ):
            warnings.warn( "The specified CSS «{}» doesn't exist. Reverting to default.".format( file_name ) )
            file_name = path.join( file_helper.get_directory( __file__ ), "default.css" )
        
        file_content = file_helper.read_all_text( file_name )
        
        host.TAG_default_style_sheet = preprocess_css( file_content, section )
    
    return host.TAG_default_style_sheet


def parse_style_sheet():
    """
    Returns a key-value dictionary from the default style-sheet.
    
    :return:    Dictionary of:
                    key   : str = Attribute name and section name as a string `section.attribute`
                    value : str = Value 
    """
    host = MENV.host
    
    if not hasattr( host, "TAG_default_style_sheet_parsed" ) or host.TAG_default_style_sheet_parsed is None:
        source = default_style_sheet()
        stage = 0
        title = None
        host.TAG_default_style_sheet_parsed = { }
        
        for line in source.split( "\n" ):
            if not stage:
                if "{" in line:
                    stage = True
                else:
                    title = [x.strip() for x in line.split( "," )]
            elif stage:
                if "}" in line:
                    stage = False
                else:
                    key, value = (x.strip( "; " ) for x in line.split( ":", 1 ))
                    
                    for key2 in title:
                        host.TAG_default_style_sheet_parsed[key2 + "." + key] = value
    
    return host.TAG_default_style_sheet_parsed


def preprocess_css( source: str, section: str, sections_receiver: Set[str] = None ) -> str:
    """
    Preprocesses the CSS given the functionality listed in the comments in `default.css`.
    
    :param source:              Css source
    :param section:             User chosen section 
    :param sections_receiver:   Optional set to receive the list of available sections
    :return:                    Preprocesses CSS. 
    """
    
    lookup_table = []
    r = []
    condition = True
    
    if sections_receiver is None:
        sections_receiver = set()
    
    for line in source.split( "\n" ):
        for k, v in lookup_table:
            line = line.replace( k, v )
        
        if line.startswith( "#" ):
            elements = line[1:].split( " " )
            elements = [x.strip() for x in elements]
            elements = [x for x in elements if x]
            name = elements[0].upper()
            
            if name == "DEFINE":
                lookup_table.append( (elements[1], elements[2]) )
            elif name == "WHEN":
                attrs = set( x.upper() for x in elements[1:] )
                sections_receiver.update( attrs )
                condition = section.upper() in attrs
        elif condition:
            r.append( line )
    
    return "\n".join( r )
