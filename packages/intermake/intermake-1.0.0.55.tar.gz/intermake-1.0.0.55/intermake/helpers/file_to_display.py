from mhelper import WriterBase
from intermake.engine.environment import MCMD


class FileToDisplayWriter( WriterBase ):
    """
    Handles writing to MCMD instead of a file.
    """


    @classmethod
    def on_describe( cls ) -> str:
        return "Writes to the currently selected user interface (i.e. the command line, GUI, or Jupyter, depending on which the user is using)."


    def __init__( self, *args, **kwargs ) -> None:
        super().__init__( *args, **kwargs )
        self.lines = []
        self.closed = False
    
    
    def __enter__( self ):
        return self
    
    
    def __exit__( self, exc_type, exc_val, exc_tb ):
        self.close()
    
    
    def write( self, text ) -> None:
        if self.closed:
            raise ValueError( "Virtual stream has already been closed." )
        
        self.lines.append( text )
    
    
    def close( self ) -> None:
        if self.closed:
            return
        
        for line in self.lines:
            MCMD.print( line )
        
        self.closed = True
    
    
    def __repr__( self ):
        return "FileToDisplayWriter"
