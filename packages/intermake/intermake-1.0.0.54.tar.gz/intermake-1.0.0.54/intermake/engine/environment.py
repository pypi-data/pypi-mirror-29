import inspect
from typing import Optional, List, Union, Tuple, cast, Dict

from intermake.engine import constants

from mhelper import SimpleProxy, NOT_PROVIDED, FrozenAttributes

from intermake.datastore.local_data import LocalData
from intermake.engine.mandate import Mandate
from intermake.engine.plugin_manager import PluginManager
from intermake.hosts.base import PluginHost, DMultiHostProvider, create_simple_host_provider_from_class, RunHostArgs, ERunMode, ERunStatus
from intermake.visualisables.visualisable import IVisualisable, UiInfo, EColour
from intermake.hosts.frontends.gui_qt.designer.resource_files import resources


_Plugin_ = "intermake.engine.plugin.Plugin"


class _DefaultRoot( IVisualisable ):
    def visualisable_info( self ) -> "UiInfo":
        return UiInfo( name = MENV.abv_name,
                       comment = MENV.name,
                       type_name = "application",
                       value = "",
                       colour = EColour.CYAN,
                       icon = resources.app,
                       extra_named = [MENV.plugins.plugins()] )


class __Environment( FrozenAttributes ):
    """
    The Intermake environment, accessed through the global variable `MENV`.
    
    For consistency of documentation, all fields are accessed through properties, please see the
    documentation on these properties for details on what can be accessed through MENV.
    """
    
    
    def __init__( self ) -> None:
        """
        CONSTRUCTOR
        """
        self.__name: str = constants.DEFAULT_NAME
        self.__version: str = "0.0.0.0"
        self.__abbreviated_name: Optional[str] = None
        self.__root: Optional[IVisualisable] = _DefaultRoot()
        self.__constants: Dict[str, str] = { }
        self.__plugins: PluginManager = PluginManager()
        self.__local_data: LocalData = LocalData()
        self.__host_provider: DMultiHostProvider = None
        self.__host: PluginHost = None
        self.__is_locked: bool = False
        
        self.__constants["APP_NAME"] = SimpleProxy( lambda: self.name )
        self.__constants["APP_ABV"] = SimpleProxy( lambda: self.abv_name )
        self.__constants["APP_VERSION"] = SimpleProxy( lambda: self.version )
        self.__constants["DATA_FOLDER"] = SimpleProxy( lambda: self.local_data.get_workspace() + "/" )
        
        super().__init__()
    
    
    def configure( self,
                   *,
                   name: str = NOT_PROVIDED,
                   abv_name: Optional[str] = NOT_PROVIDED,
                   version: Union[str, List[int], Tuple[int]] = NOT_PROVIDED,
                   root: Optional[IVisualisable] = NOT_PROVIDED,
                   host_provider: DMultiHostProvider = NOT_PROVIDED,
                   using: str = None,
                   allow_lock: bool = True,
                   ):
        """
        Initialises or reconfigures the Intermake environment.
        
        :param name:            Sets the name of the application.
                                Note that `MENV.constants["APP_NAME"]` is by bound by default to this property.
        :param abv_name:        Sets the abbreviated name.
                                Used in place of the application name in certain places, such as the command line display and the defualt application's data folder.
                                If this is `None`, the non-abbreviated :param:`name` is returned.
                                Note that `MENV.constants["APP_ABV"]` is by bound by default to this property. 
        :param version:         Sets The application version.
                                If this starts with a `0.`, intermake will assume this is an alpha version and include a warning message in the application's banner.
                                Note that `MENV.constants["APP_VERSION"]` is by bound by default to this property.
        :param root:            The application root object.
                                This is an IVisualisable derived object which allows the user to traverse a virtual application hierarchy.
                                Setting this to `None` restores the default root object, which disables the application hierarchy in most cases.
                                See class: `IVisualisable`.   
        :param host_provider:   (advanced!) The host provider.
                                This is used by the :function:`ui` core commands to suggest a new host for the various UI modes.
                                `None` assumes the default.
        :param using:           (advanced!) If the application has already been setup, :param:`using` must be set to the name of the application, otherwise
                                :param:`allow_lock` is followed.
        :param allow_lock:      (advanced!) If the application has already been setup, and :param:`using` is not set, then all changes
                                are ignored and the plugin set is frozen to prevent further changes. This allows one Intermake application
                                to import another Intermake application as a library without the second application overriding the first
                                (unless it explicitly sets :param:`using`). Turning :param:`allow_lock` off prevents environment locking
                                and instead causes a `SystemExit` error. Set :param:`allow_lock` off if your application make complex
                                changes to the environment such that it cannot be used as a library.
        :return:                `True` if the values were set.
                                If the return value is `False` the caller should assume they are being called as library.
                                Plugin registration is automatically suppressed in this case, but the caller should take care to avoid
                                other changes that would affect the UI, such adding coercers and visualisers to the global state.
        """
        # Locked?
        if (using and using != self.__name) or (not using and self.__name != constants.DEFAULT_NAME):
            self.__is_locked = True
            
            if allow_lock:
                return False
            else:
                message = "An application named «{}» is attempting to setup the environment named «{}», but the environment is currently named «{}». Please see the 'Troubleshooting: locked environment' section of Intermake's readme for details.".format( name, using, self.name )
                raise ValueError( message )
        
        self.__is_locked = False
        
        # Name
        if name is not NOT_PROVIDED:
            self.__name = name
        
        if not self.__name or self.__name == constants.DEFAULT_NAME:
            raise ValueError( "An application name must be provided, the name «{}» is invalid.".format( self.__name ) )
        
        # Host provider
        if host_provider is not NOT_PROVIDED:
            self.__host_provider = host_provider
        
        # Version
        if version is not NOT_PROVIDED:
            if not isinstance( version, str ):
                version = ".".join( str( x ) for x in version )
            
            self.__version = version
        
        # Root
        if root is not NOT_PROVIDED:
            self.__root = root
        
        # Abbreviated name
        if abv_name is not NOT_PROVIDED:
            self.__abbreviated_name = abv_name
        
        return True
    
    
    @property
    def is_locked( self ) -> bool:
        """
        State that holds the result of the last call to `init`.
        """
        return self.__is_locked
    
    
    @property
    def name( self ) -> str:
        """
        Gets the name of the application.
        """
        return self.__name
    
    
    @property
    def plugins( self ) -> PluginManager:
        """
        Gets the `PluginManager`, that allows you to view available plugins and register new ones.
        See class: PluginManager
        """
        return self.__plugins
    
    
    @property
    def local_data( self ) -> LocalData:
        """
        Obtains the `LocalData` store, used to apply and retrieve application settings.
        """
        return self.__local_data
    
    
    @property
    def constants( self ) -> Dict[str, str]:
        """
        Obtains the constant dictionary, used to replace text `"$(XXX)"` in documentation strings, where `XXX` is the name of a key from this dictionary.
        
        Dictionary keys:        Variable to find
        Dictionary values:      Text to replace. This can be any object coercible via `str`, thus the dictionary supports dynamic values.
        """
        return self.__constants
    
    
    @property
    def host( self ) -> PluginHost:
        """
        Gets or sets the current plugin host.
        See class: `PluginHost`.
        """
        return self.__host
    
    
    @host.setter
    def host( self, value: PluginHost ):
        self.__host = value
    
    
    @property
    def root( self ) -> Optional[IVisualisable]:
        """
        Gets or sets the application root. 
        """
        if self.__root is None:
            self.__root = _DefaultRoot()
        
        return self.__root
    
    
    @property
    def host_provider( self ) -> DMultiHostProvider:
        """
        Gets the host provider.
        See field: `DMultiHostProvider`.
        """
        if self.__host_provider is None:
            from intermake.hosts.console import ConsoleHost
            
            def __gui() -> PluginHost:
                from intermake.hosts.gui import GuiHost
                return GuiHost()
            
            
            self.__host_provider = create_simple_host_provider_from_class( ConsoleHost, __gui )
        
        return cast( DMultiHostProvider, self.__host_provider )
    
    
    @property
    def version( self ) -> str:
        """
        Gets the application version. 
        """
        return self.__version
    
    
    @property
    def abv_name( self ) -> str:
        """
        Gets the abbreviated name of the application.
        """
        return self.__abbreviated_name or self.name


# noinspection SpellCheckingInspection
MENV: __Environment = __Environment()
"""
Obtains a read/write reference to the intermake environment.

Please see the `__Environment` documentation for the actual member list and descriptions!
"""


def __current_mandate() -> Mandate:
    """
    See field: `MCMD`.
    """
    if MENV.host is None:
        return cast( Mandate, None )
    
    return MENV.host.get_mandate()


# noinspection SpellCheckingInspection
MCMD: Mandate = SimpleProxy( __current_mandate )
"""
Obtains a copy to the current mandate, which abstracts functionality such as "print" (MCMD.print) so that the output is sent to the correct place (e.g. GUI or CLI).

Please see the `Mandate` class documentation in `intermake/engine/mandate.py` for the actual member list and descriptions!
"""


def start( caller: Optional[str] = None ):
    """
    Quickly starts up the appropriate intermake UI.
    
    :param caller:        Name of caller (i.e. __name__), used to start the CLI (ERunMode.ARG) if this is "__main__".
                          * If you have added your own check, or wish to force the CLI to start, then you do not need to supply this argument.
                          * If you do not wish the CLI to start, do not call this function!
    """
    if MENV.name == constants.DEFAULT_NAME:
        raise ValueError( "Preventing `quick_start` call without setting the `MENV.name`: This probably means that your `__init__` has not been called." )
    
    if caller is None or caller == "__main__":
        from intermake.plugins import common_commands
        common_commands.start_ui( ERunMode.ARG )


def register( plugin: _Plugin_ ) -> None:
    """
    This is a convenience function which wraps to MENV.plugins.register.
    :param plugin:  Plugin to register
    """
    # We can't just call MENV.plugins.register directly because it will look like this module
    # is the origin of the plugin, so we need to specify the module explicitly.
    frame = inspect.stack()[1]
    module_ = inspect.getmodule( frame[0] )
    
    # Register the plugin
    MENV.plugins.register( plugin, module_ )


def run_jupyter( import_: str ) -> None:
    """
    Convenience command equivalent to `ui pyi`
    """
    __import__( import_ )
    MENV.host.on_status_changed( ERunStatus.STOP )
    MENV.host = MENV.host_provider( ERunMode.JUP )
    MENV.host.on_status_changed( ERunStatus.RUN )
    MENV.host.run_host( RunHostArgs() )
