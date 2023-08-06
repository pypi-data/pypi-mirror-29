"""
Houses the PluginManager and PluginFolder classes.
"""

import inspect
from importlib import import_module
# noinspection PyUnresolvedReferences
from types import ModuleType
from typing import List, cast, Any, Dict, Iterator, Optional, Union, Tuple, Set
from warnings import warn

from intermake.plugins.visibilities import VisibilityClass
from mhelper import file_helper, string_helper, module_helper, SwitchError

from intermake.engine import constants
from intermake.hosts.frontends.gui_qt.designer.resource_files import resources
from intermake.visualisables.visualisable import EColour, IVisualisable, UiInfo


__author__ = "Martin Rusilowicz"
_Plugin_ = "intermake.engine.plugin.Plugin"
_PluginFolder_ = "intermake.engine.plugin_manager.PluginFolder"
TModule = Union[ModuleType, str]
TPluginOrModuleOrList = Union[ModuleType, _PluginFolder_, _Plugin_, List[Union[ModuleType, _PluginFolder_, _Plugin_]], Tuple[Union[ModuleType, _PluginFolder_, _Plugin_]]]


class PluginManagerProxy:
    def __init__( self, manager: "PluginManager" ):
        object.__setattr__( self, "__manager", manager )
    
    
    def __getattr__( self, item ):
        manager = object.__getattribute__( self, "__manager" )
        
        for plugin in manager.all_plugins():
            if plugin.name == item:
                return plugin
        
        raise AttributeError( "There is no plugin with the name «{}».".format( item ) )
    
    
    def __setattr__( self, key, value ):
        raise AttributeError( "PluginManagerProxy is immutable and cannot be modified." )
    
    
    def __iter__( self ):
        manager = object.__getattribute__( self, "__manager" )
        return iter( manager.all_plugins() )


class PluginManager:
    """
    Manages the set of user-defined functions formally identified as "plugins"
    
    :attribute _plugins_root:               PluginFolder that holds all the registered plugins
    :attribute __namespace:                 Some arbitrary text we prefix on the front of all registered plugin folder names.
                                            This is only used to track user-imports via the `import_` command, so it is usually `None`.
    :attribute __namespace_visibilities:    `VisibilityClass`es associated with the `__namespace`, usually empty.
    :attribute __all_plugins:               List of all registered plugins
    """
    
    
    def __init__( self ) -> None:
        """
        CONSTRUCTOR
        """
        self.plugins_root = PluginFolder( constants.EXPLORER_KEY_PLUGINS, "All loaded Plugins", None )
        self.__namespace = None
        self.__namespace_visibilities = { }
        self.__all_plugins = []
    
    
    @property
    def namespace( self ) -> str:
        """
        Gets or sets the namespace.
        This string is prefixed onto the front of all newly registered plugin folder names.
        It is usually empty.
        When set, all newly registered plugins are automatically put into a `VisibilityClass` of the same name.
        """
        return self.__namespace
    
    
    @namespace.setter
    def namespace( self, value: str ) -> None:
        self.__namespace = value
        
        if value and value not in self.__namespace_visibilities:
            self.__namespace_visibilities[value] = VisibilityClass( name = value, is_functional = True, is_visible = False )
    
    
    def get_proxy( self ):
        return PluginManagerProxy( self )
    
    
    def to_dictionary( self ) -> Dict[str, _Plugin_]:
        """
        Returns a dictionary of the plugins.
        :return: 
        """
        from intermake.engine.plugin import Plugin
        
        r: Dict[str, Plugin] = { }
        
        # Names to avoid overriding, we don't want to override `exit` but we do want to
        # override `help`.
        avoid = ["exit"]
        
        for x in self.all_plugins():  # type: Plugin
            if x.is_visible:
                for n in x.names:
                    if n not in avoid:
                        r[n] = x
        
        return r
    
    
    def find_visibilities( self ) -> Set[VisibilityClass]:
        result = set()
        
        for plugin in self:
            plugin_visibilities = { plugin.visibility_class }
            
            while plugin_visibilities:
                result.update( plugin_visibilities )
                
                new_visibilities = set()
                
                for visibility in plugin_visibilities:
                    if visibility.parents:
                        for parent in visibility.parents:
                            new_visibilities.add( parent )
                
                plugin_visibilities = new_visibilities
        
        return result
    
    
    def register( self, plugin: _Plugin_, module_: Optional[TModule] = None ):
        """
        Registers a plugin.
        
        :remarks:
        The plugin will not be registered if the :global:`MENV` is locked.
        
        :param module_:  Module to register under. If `None` uses the calling module. 
        :param plugin:   Plugin to register.
        """
        from intermake.engine.plugin import Plugin
        assert isinstance( plugin, Plugin )
        
        from intermake.engine.environment import MENV
        if MENV.is_locked:
            # Prevent registering new plugins if the environment is locked
            return
        
        if module_ is None:
            frame = inspect.stack()[1]
            module_ = inspect.getmodule( frame[0] )
        
        if inspect.ismodule( module_ ):
            module_name, module_docs = self.__module_name_and_docs( module_ )
        else:
            module_name = module_
            module_docs = None
        
        if plugin.folder:
            module_name = plugin.folder
        
        if self.__namespace:
            module_name = self.__namespace + "/" + module_name
            plugin.visibility_class = self.__namespace_visibilities[self.__namespace] & plugin.visibility_class
        
        from intermake.engine.plugin import Plugin
        
        assert isinstance( plugin, Plugin )
        
        # Check that it isn't already registered
        if plugin in self.__all_plugins or plugin.parent:
            raise KeyError(
                    "The plugin «{0}» is exported by both \"{1}\" and \"{2}\". Check that you haven't accidentally re-exported a plugin imported from another module. Did you use accidentally `import x.y` instead of `import x`?".format(
                            plugin.name,
                            plugin.parent,
                            module_ ) )
        
        # Add the plugin itself
        folder = self.__register_folder( module_docs, module_name )
        plugin.parent = folder
        folder.add_child( plugin )
        self.__all_plugins.append( plugin )
        
        # Fix the names
        for ex_plugin in self.all_plugins():
            if ex_plugin is not plugin:
                conflicts = []
                
                for name_1 in plugin.names:
                    if name_1 in ex_plugin.names:
                        conflicts.append( name_1 )
                
                for conflict in list( conflicts ):
                    ex_plugin.names.remove( conflict )
                    
                    if len( ex_plugin.names ) == 0:
                        ex_plugin.names.append( "cmd_{}".format( id( ex_plugin ) ) )
                    else:
                        conflicts.remove( conflict )
                
                if conflicts:
                    if plugin.parent == ex_plugin.parent:
                        msg = "There are two plugins with the name «{}» exported by the module «{}». This is probably a mistake and so an error has been raised.".format(
                                conflicts[0],
                                plugin.parent )
                        
                        raise ValueError( msg )
                    else:
                        msg = "There are two plugins with the name «{}», one exported by the module «{}» and another by the module «{}». The original plugin has been renamed to \"{}\". This looks like the plugins just have the same name, but check that you haven't accidentally re-exported a plugin imported from another module.".format(
                                conflicts[0],
                                plugin.parent,
                                ex_plugin.parent,
                                ex_plugin.name )
                        
                        warn( msg, UserWarning )
    
    
    @staticmethod
    def legacy_load_namespace( namespace: TModule ):
        """
        Utility function that loads all modules in a namespace.
        This replaces old _register-all-in-namespace_ type functions that are now replaced by plugin self-registration.
        """
        module_helper.load_namespace( namespace )
    
    
    def __register_folder( self, docs: str, name: str ):
        for folder in self.plugins_root.contents:  # type: PluginFolder
            if folder.name == name:
                if docs:
                    if docs not in folder.description:
                        folder.description += "\n\n" + docs
                
                return folder
        
        folder = PluginFolder( name, docs, self.plugins_root )
        self.plugins_root.contents.append( folder )
        return folder
    
    
    @staticmethod
    def __module_name_and_docs( module_: TModule ):
        if isinstance( module_, str ):
            module_ = import_module( module_ )
        
        doc = module_.__doc__
        path = module_helper.get_module_path( module_ )
        
        if doc:
            doc = doc.strip() + "\n\n"
        else:
            doc = ""
        
        doc += "This module contains the set of plugins from `" + path + "`:"
        
        name = file_helper.get_filename_without_extension( path )
        name = string_helper.undo_camel_case( name, "_" )
        
        for attr in ["mcmd_folder_name", "_mcmd_folder_name_", "__mcmd_folder_name__"]:
            name = getattr( module_, attr, name )
        
        return name, doc
    
    
    def __iter__( self ) -> "Iterator[.engine.plugin.Plugin]":
        """
        OVERRIDE 
        """
        return iter( self.all_plugins() )
    
    
    def plugins( self ) -> "PluginFolder":
        return self.plugins_root
    
    
    @classmethod
    def __iterate( cls, x ):
        from intermake.engine.plugin import Plugin
        
        if isinstance( x, Plugin ):
            yield x
            
            for c in x.children():
                yield from cls.__iterate( c )
        
        elif isinstance( x, PluginFolder ):
            for c in x.contents:
                yield from cls.__iterate( c )
        else:
            raise SwitchError( "x", x )
    
    
    def all_plugins( self ) -> "List[.engine.plugin.Plugin]":
        from intermake.engine.plugin import Plugin
        return cast( List[Plugin], self.__all_plugins )


class PluginFolder( IVisualisable ):
    """
    A collection of plugins organised into a folder.
    """
    
    
    def __init__( self, name: str, doc: str, parent: "Optional[PluginFolder]" ) -> None:
        """
        Constructor
        :param name:    Folder name 
        :param doc:     Documentation 
        :param parent:  Parent folder (if any) 
        """
        self.name = name
        self.contents = []
        self.description = doc
        self.parent = parent
    
    
    def visualisable_info( self ) -> UiInfo:
        """
        OVERRIDE 
        """
        num_plugins = len( self )
        num_modules = sum( isinstance( x, PluginFolder ) for x in self.contents )
        
        if num_modules:
            if num_plugins != num_modules:
                text = "{0} plugins".format( num_plugins )
            else:
                text = "{0} modules".format( num_modules )
        else:
            if num_plugins:
                text = "{0} plugins".format( num_plugins )
            else:
                text = "No plugins".format( num_plugins )
        
        return UiInfo( name = self.name,
                       comment = self.description,
                       type_name = constants.VIRTUAL_FOLDER,
                       value = text,
                       colour = EColour.YELLOW,
                       icon = resources.folder,
                       extra_named = self.contents )
    
    
    def __len__( self ) -> int:
        """
        OVERRIDE 
        """
        return len( self.contents )
    
    
    def __iter__( self ) -> "Iterator[.intermake.engine.plugin.Plugin]":
        """
        OVERRIDE 
        """
        from intermake.engine.plugin import Plugin
        yield from (x for x in self.contents if isinstance( x, Plugin ))
    
    
    def __str__( self ):
        """
        OVERRIDE 
        """
        return self.name
    
    
    def add_child( self, child_plugin ):
        """
        :type child_plugin: Union[Plugin, PluginFolder]
        """
        self.contents.append( child_plugin )
    
    
    def remove_child( self, child_plugin ):
        """
        :type child_plugin: Union[Plugin, PluginFolder]
        """
        self.contents.remove( child_plugin )
