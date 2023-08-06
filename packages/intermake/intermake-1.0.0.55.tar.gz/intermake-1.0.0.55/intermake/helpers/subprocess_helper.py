import re
from typing import Sequence, List, Optional, Callable, Pattern

from intermake.engine.constants import EStream
from intermake.engine.environment import MCMD
from mhelper import async_helper, SubprocessError


DStrReceiver = Callable[[str], None]


class __SubprocessRun:
    def __init__( self,
                  title: str,
                  garbage: List[Pattern],
                  collect_stdout: Optional[DStrReceiver],
                  hide: bool ):
        self.garbage = garbage
        self.collect_stdout = collect_stdout
        self.is_blank = [True, True]
        self.hide = hide
        
        if hide:
            self.action = MCMD.action( title ).__enter__()
    
    
    def close( self ):
        if self.hide:
            self.action.__exit__()
    
    
    def __print( self, text, stream, stream_index ):
        if self.hide:
            self.action.increment()
            return
        
        if any( y.search( text ) for y in self.garbage ):
            return
        
        if not text:
            if self.is_blank[stream_index]:
                return
            
            self.is_blank[stream_index] = True
        else:
            self.is_blank[stream_index] = False
        
        MCMD.print( text, stream = stream )
    
    
    def print_1( self, x ):
        self.__print( x, EStream.EXTERNAL_STDOUT, 0 )
        if self.collect_stdout is not None:
            self.collect_stdout( x )
    
    
    def print_2( self, x ):
        self.__print( x, EStream.EXTERNAL_STDERR, 1 )


def run_subprocess( command: Sequence[str],
                    *,
                    garbage: Optional[List[str]] = None,
                    inspect = False,
                    collect_stdout: Optional[DStrReceiver] = None,
                    hide: bool = False ):
    """
    Runs the specified subprocess
    
    :param hide:                Hide output (displays progress bar instead) 
    :param collect_stdout:      Function to receive std-out.
    :param inspect:             When true, halts for errors.
    :param command:             Commands and arguments
    :param garbage:             List containing one or more regex that specify lines dropped from display 
    """
    if garbage is None:
        garbage: List[str] = []
    
    garbage: List[Pattern] = [re.compile( x ) for x in garbage]
    
    spr = __SubprocessRun( " ".join(command), garbage, collect_stdout, hide )
    
    try:
        async_helper.async_run( command, spr.print_1, spr.print_2, check = True )
    except SubprocessError:
        if inspect:
            MCMD.question( "Halting to inspect subprocess error", [None], None )
        else:
            raise
    finally:
        spr.close()
