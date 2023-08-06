from typing import List, Dict, Callable, Optional
import sys

from mhelper import string_helper, ansi
from mhelper.comment_helper import ignore


DTarget = Callable[[str], None]


def default_logger( text: str ) -> None:
    """
    The default logging target.
    This function may be replaced or modified.
    """
    print( text, file = sys.stderr )


def set_default_logger( target: DTarget ) -> None:
    """
    Convenience method that sets `default_logger`.
    """
    # noinspection PyGlobalUndefined
    global default_logger
    default_logger = target


_INDENT_SIZE = 4


class Logger:
    """
    Logging simplified.
    
    Usage:
    
    To create:      `log = Logger("my logger", True)`
    To log:         `log("hello, world")`
    To log details: `log("hello {}", x)` (does not need to `format` unless enabled)
    To pause:       `log.pause("hello world")`
    To query:       `if log` or `if log.enabled`
    """
    
    
    def __init__( self, name: str,
                  enabled: bool = False,
                  defaults: Dict[str, object] = None,
                  target: DTarget = None ):
        """
        CONSTRUCTOR
        :param name:    Default value to :property:`name`. 
        :param enabled:    Default value to :property:`enabled`.
        :param defaults:    Default values to :method:`format`.
        :param target:      Default value for :property:`target`. 
        """
        LOGGERS.append( self )
        self.name = name
        
        self.__indent = 0
        self.__prefix = ""
        self.__update_prefix()
        
        self.__target = None
        self.__enabled = enabled
        self.target: DTarget = target
        self.__skip = set()
        self.defaults = defaults or { }
    
    
    def __update_prefix( self ):
        self.__prefix = self.name + ": " + (" " * (self.__indent * _INDENT_SIZE))
    
    
    def __bool__( self ):
        return self.__enabled
    
    
    def pause( self, message = "PAUSED", *args, key = None ):
        if not self.__enabled:
            return
        
        if key and key in self.__skip:
            return
        
        message = self.format( message, *args )
        
        c = ansi.FORE_BRIGHT_WHITE + ansi.BACK_BLUE
        r = ansi.RESET
        
        # C continue
        # D disable
        # A always skip
        # B break
        
        if key is None:
            print( message + " " + c + "[BCD]" + r, end = "", file = sys.stderr )
        else:
            print( message + " " + c + "[ABCD]" + r, end = "", file = sys.stderr )
        
        i = input()
        
        if i == "a" and key:
            self.__skip.add( key )
        elif i == "d":
            self.target = None
        elif i == "b":
            import pdb
            pdb.set_trace()
    
    
    @property
    def enabled( self ) -> bool:
        """
        Gets or sets whether the logger is enabled.
        """
        return self.__enabled
    
    
    @enabled.setter
    def enabled( self, value: bool ):
        self.__enabled = value
    
    
    @property
    def target( self ) -> DTarget:
        """
        Gets or sets the target printer, `DTarget`.
        Setting this to `None` assumes the default target (stderr).
        :return: 
        """
        return self.__target
    
    
    @target.setter
    def target( self, target: Optional[DTarget] ):
        if target is None:
            self.__target = default_logger
        else:
            self.__target = target
    
    
    def __call__( self, *args, **kwargs ):
        if not self.__enabled:
            return self
        
        self.print( self.format( *args, *kwargs ) )
        
        return self
    
    
    def format( self, *args, key: object = None, **kwargs ):
        ignore( key )
        
        true_kwargs = dict( self.defaults )
        true_kwargs.update( kwargs )
        
        if len( args ) == 1:
            return args[0]
        elif len( args ) > 1:
            vals = list( args[1:] )
            for i in range( len( vals ) ):
                v = vals[i]
                
                if type( v ) in (set, list, tuple, frozenset):
                    vals[i] = string_helper.format_array( v, **true_kwargs )
                
                vals[i] = "«" + str( vals[i] ) + "»"
            
            return args[0].format( *vals )
    
    
    def print( self, message ):
        if not self.__enabled:
            return
        
        if "\n" in message:
            for i, split in enumerate( message.split( "\n" ) ):
                self.print( ("\b\b: " if i != 0 else "") + split )
            
            return
        
        self.__target( ansi.DIM + self.__prefix + ansi.RESET + string_helper.highlight_quotes( message, "«", "»", ansi.FORE_YELLOW, ansi.RESET ) )
    
    
    @property
    def indent( self ):
        return self.__indent
    
    
    @indent.setter
    def indent( self, level: int ):
        assert isinstance(level, int)
        self.__indent = level
        self.__update_prefix()
    
    
    def __enter__( self ):
        self.indent += 1
    
    
    def __exit__( self, exc_type, exc_val, exc_tb ):
        self.indent -= 1


LOGGERS: List[Logger] = []
"""List of all loggers"""
