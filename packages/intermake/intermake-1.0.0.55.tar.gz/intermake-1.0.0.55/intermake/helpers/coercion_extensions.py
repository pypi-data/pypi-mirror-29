from typing import Optional, Dict, Union, Type

import stringcoercion
from mhelper import exception_helper
from stringcoercion import Coercer, CoercionInfo, CoercionError

from intermake.visualisables.visualisable import IVisualisable, NamedValue
from intermake.visualisables.visualisable_operations import PathToVisualisable
from intermake.plugins import console_explorer


class _VisualisableCoercionSettings:
    """
    A class which may be used to control the Visualisable coercions.
    """
    
    
    def __init__( self ):
        self.__auto_search: Dict[Type[IVisualisable], str] = { }
        self.treat_as_visualisable = []
    
    
    def register_as_visualisable( self, type_: type ):
        self.treat_as_visualisable.append( type_ )
    
    
    def register_auto_search( self, type_: Type[IVisualisable], path: Union[str, PathToVisualisable] ) -> None:
        """
        For `IVisualisable`s of the specified type, the specified path will be searched when the user
        types its name or number.
        :param type_:   Type to register 
        :param path:    Path to search
        """
        if not isinstance( path, str ):
            if not isinstance( path, PathToVisualisable ):
                raise exception_helper.type_error( "path", path, Union[str, PathToVisualisable] )
            
            path = str( path )
        
        self.__auto_search[type_] = path
    
    
    def _get_auto_search( self, type_: Type[IVisualisable] ):
        ext = self.__auto_search.get( type_ )
        
        if ext:
            return PathToVisualisable.SEP + ext
        else:
            return None


VISUALISABLE_COERCION = _VisualisableCoercionSettings()
"""
An object which may be used to control the Visualisable coercions.
See `_VisualisableCoercionSettings`.
"""


def coerce_visualisable( text: str, type_: Type[IVisualisable] ):
    if not issubclass( type_, IVisualisable ):
        assert type_ in VISUALISABLE_COERCION.treat_as_visualisable, type_
        restrict = NamedValue
    else:
        restrict = type_
    
    ext = VISUALISABLE_COERCION._get_auto_search( type_ )
    
    if not PathToVisualisable.SEP in text and ext:
        text = ext + text
    
    r = console_explorer.follow_path( path = text, restrict = restrict )
    assert r is not None
    
    if not issubclass( type_, IVisualisable ):
        last = r.get_last()
        assert isinstance( last, NamedValue ), last
        if not isinstance( last.value, type_ ):
            raise CoercionError( "Select visualisable failed. This argument requires a «{}», but you have selected «{}», which is a «{}».".format( type_, r, type( last ) ), cancel = True )
    
    return r


class _VisualisableCoercion( Coercer ):
    """
    **Visualisables** may be referenced by providing their _path_ in the object hierarchy.
    """
    def coerce( self, info: CoercionInfo ) -> Optional[object]:
        type_ = info.annotation.value
        r = coerce_visualisable( info.source, type_ ).get_last()
        
        if type_ in VISUALISABLE_COERCION.treat_as_visualisable:
            assert isinstance( r, NamedValue ), r
            r = r.value
        
        return r
    
    
    def can_handle( self, info: CoercionInfo ):
        if info.annotation.is_directly_below( IVisualisable ):
            return self.PRIORITY.LOW
        
        if any( info.annotation.is_directly_below( x ) for x in VISUALISABLE_COERCION.treat_as_visualisable ):
            return self.PRIORITY.LOW
        
        return self.PRIORITY.SKIP


class _VisualisablePathCoercion( Coercer ):
    def coerce( self, info: CoercionInfo ) -> Optional[object]:
        return coerce_visualisable( info.source, info.annotation.value.type_restriction() )
    
    
    def can_handle( self, info: CoercionInfo ):
        return info.annotation.is_directly_below( PathToVisualisable )


class _MAnnotationCoercer( Coercer ):
    def coerce( self, args: CoercionInfo ):
        return args.collection.coerce( args.annotation.mannotation_arg, args.source )  # the result is the type, not the annotation!
    
    
    def can_handle( self, info: CoercionInfo ):
        return info.annotation.is_mannotation


# Register them
stringcoercion.get_default_coercer().register( _VisualisableCoercion(), _VisualisablePathCoercion(), _MAnnotationCoercer() )
