from intermake.engine.async_result import AsyncResult


class IGuiPluginHostWindow:
    def plugin_completed( self, result: AsyncResult ) -> None:
        raise NotImplementedError( "abstract" )
    
    def return_to_console( self ) -> bool:
        raise NotImplementedError( "abstract" )