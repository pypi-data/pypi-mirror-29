from typing import Optional, Union, Type, Any


from editorium.editorium_qt import Editor_TextBrowsableBase, EditorInfo
from intermake.visualisables.visualisable import IVisualisable
from intermake.visualisables.visualisable_operations import PathToVisualisable
from intermake.plugins import console_explorer


TVis = Union[IVisualisable, PathToVisualisable]


def _browse( window: Any, type_: type ):
    from intermake.hosts.frontends.gui_qt.frm_tree_view import FrmTreeView
    
    return FrmTreeView.request( window,
                                "Select " + type_.__name__,
                                None,
                                lambda x: isinstance( x.get_value(), type_ ) )


class Editor_Visualisable( Editor_TextBrowsableBase ):
    """
    Edits:  IVisualisable 
    """
    
    
    def __init__( self, info: EditorInfo ):
        super().__init__( info )
        self.visualisable_type = self.info.inspector.type_or_optional_type
        self.last_path = None
        self.fixed_value = None
    
    
    @classmethod
    def can_handle( cls, info: EditorInfo ) -> bool:
        return info.inspector.is_directly_below_or_optional( IVisualisable )
    
    
    def on_browse( self, value: IVisualisable ) -> Optional[IVisualisable]:
        path = _browse( self.editor.window(), self.visualisable_type )
        
        if path is None:
            return None
        
        self.fixed_value = None
        self.last_path = path
        return path.get_last()
    
    
    def on_convert_to_text( self, value: IVisualisable ):
        assert isinstance( value, IVisualisable ), value
        
        if self.last_path is not None and value is self.last_path.get_last():
            self.fixed_value = None
            return str(self.last_path)
        
        self.last_path = None
        self.fixed_value = value
        return value.visualisable_info().name
    
    
    def on_convert_from_text( self, text: str ) -> object:
        if self.fixed_value is not None and text == self.fixed_value.visualisable_info().name:
            return self.fixed_value
        
        path: PathToVisualisable = console_explorer.follow_path( path = text, restrict = self.visualisable_type )
        self.last_path = path
        self.fixed_value = None
        return path.get_last()


class Editor_VisualisablePath( Editor_TextBrowsableBase ):
    """
    Edits:  PathToVisualisable[T] 
    """
    
    
    def __init__( self, info: EditorInfo ):
        super().__init__( info )
        
        self.visualisable_type = self.info.inspector.type_or_optional_type.type_restriction()
    
    
    @classmethod
    def can_handle( cls, info: EditorInfo ) -> bool:
        return info.inspector.is_directly_below_or_optional( PathToVisualisable )
    
    
    def on_browse( self, value: IVisualisable ) -> Optional[PathToVisualisable]:
        return _browse( self.editor.window(), self.visualisable_type )
    
       
    
    def on_convert_from_text( self, text: str ) -> object:
        return console_explorer.follow_path( path = text, restrict = self.visualisable_type )
