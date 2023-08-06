"""
Helper functions for reading and writing.
"""
import os
import sys
import tempfile
import warnings
from typing import Dict, Optional, TextIO, Type, TypeVar, Union, cast

from mhelper.comment_helper import abstract, override, virtual
from mhelper.special_types import NOT_PROVIDED


T = TypeVar( "T" )


def load_npy( file_name ):
    """
    Loads an NPY file. If it is an NPZ this extracts the `data` value automatically.
    Requires the :library:`numpy`.
    """
    # noinspection PyPackageRequirements
    import numpy
    result = numpy.load( file_name, allow_pickle = False, fix_imports = False )
    
    if file_name.upper().endswith( ".NPZ" ):
        result = result["data"]
    
    return result


def load_npz( file_name ):
    """
    Loads an NPZ file and returns the `data` value.
    Requires the :library:`numpy`.
    """
    
    # noinspection PyPackageRequirements
    import numpy
    result = numpy.load( file_name, allow_pickle = False, fix_imports = False )
    result = result["data"]
    
    return result


def save_bitarray( file_name: str, value ) -> None:
    """
    Saves a bit array.
    Requires the :library:`bitarray`.
    
    :type value: bitarray
    
    :param file_name: File name
    :param value: Value to save
    """
    # noinspection PyPackageRequirements
    from bitarray import bitarray
    from mhelper.exception_helper import SubprocessError
    from mhelper import exception_helper, file_helper
    
    exception_helper.assert_instance( "save_bitarray::value", value, bitarray )
    assert isinstance( value, bitarray )
    
    try:
        with open( file_name, "wb" ) as file_out:
            value.tofile( file_out )
    except TypeError:
        # Stupid "open file expected" error on OSX (due to bug writing large files - fallback to manual implementation)
        _save_bytes_manually( file_name, value.tobytes() )
    except Exception as ex:
        raise SubprocessError( "Failed to write bitarray of length {} to «{}».".format( len( value ), file_name ) ) from ex
    
    size = float( file_helper.file_size( file_name ) )
    expected = len( value )
    
    if size < expected / 8.0:
        raise ValueError( "Saved file is shorter ({} bytes or {} bits) than the originating bitarray ({} bytes or {} bits).".format( size, size * 8, expected / 8, expected ) )


def _save_bytes_manually( file_name: str, value: bytes ):
    """
    Fallback function used by :func:`save_bitarray`.
    """
    warnings.warn( "Save bitarray failed. This is probably due to an error in your `bitarray` library. The file will be saved incrementally but this will take longer.", UserWarning )
    BATCH_SIZE = 100000
    cursor = 0
    length = len( value )
    
    with open( file_name, "wb" ) as file_out:  # note that writing large arrays on OSX is probably the problem, we can't just dump the bytes
        while cursor < length:
            next = min( cursor + BATCH_SIZE, length )
            slice = value[cursor:next]
            file_out.write( slice )
            cursor = next


def _read_bytes_manually( file_name: str ) -> bytes:
    BATCH_SIZE = 100000
    b = bytearray()
    
    with open( file_name, "rb" ) as file_in:
        while True:
            buf = file_in.read( BATCH_SIZE )
            
            if len( buf ) == 0:
                break
            
            b.extend( buf )
    
    return bytes( b )


def load_bitarray( file_name: str ):
    """
    Loads a bitarray
    :param file_name: File to read 
    :return: bitarray. Note this may be padded with missing bits. 
    """
    # noinspection PyPackageRequirements
    from bitarray import bitarray
    
    result = bitarray()
    
    try:
        with open( file_name, 'rb' ) as file_in:
            result.fromfile( file_in )
    except SystemError:  # OSX error
        result = bitarray()
        result.frombytes( _read_bytes_manually( file_name ) )
        assert len( result ) != 0
    
    return result


def save_npy( file_name, value ):
    # noinspection PyPackageRequirements
    import numpy
    
    numpy.save( file_name, value, allow_pickle = False, fix_imports = False )


def save_npz( file_name, value ):
    # noinspection PyPackageRequirements
    import numpy
    
    numpy.savez_compressed( file_name, data = value )


def load_binary( file_name: str, default: Optional[object] = NOT_PROVIDED ):
    """
    Loads a binary file
    
    :param file_name: Filename to load  
    :param default:     Whether to default the values (if `NOT_PROVIDED` an exception is raised) 
    :return: Loaded file, or `default` (if specified) 
    """
    try:
        import pickle
        
        with open( file_name, "rb" ) as file:
            return pickle.load( file, fix_imports = False )
    except Exception:
        if default is NOT_PROVIDED:
            raise
        
        return default
    except BaseException as ex:
        warnings.warn( "Loading the binary file «{}» caused a «{}» exception.".format( file_name, type( ex ).__name__ ), UserWarning )
        raise


def save_binary( file_name, value ):
    import pickle
    
    with open( file_name, "wb" ) as file:
        try:
            pickle.dump( value, file, fix_imports = False )
        except Exception as ex:
            raise IOError( "Error saving data to binary file. Filename = «{}». Data = «{}».".format( file_name, value ) ) from ex


def load_json( file_name, keys = True ):
    from mhelper.file_helper import read_all_text
    import jsonpickle
    
    text = read_all_text( file_name )
    
    return jsonpickle.decode( text, keys = keys )


def save_json( file_name, value, keys = True ):
    from mhelper.file_helper import write_all_text
    import jsonpickle
    
    write_all_text( file_name, jsonpickle.encode( value, keys = keys ) )


def default_values( target: T, default: Optional[Union[T, type]] = None ) -> T:
    if default is None:
        if target is None:
            raise ValueError( "Cannot set the defaults for the value because both the value and the defaults are `None`, so neither can be inferred." )
        
        default = type( target )
    
    if isinstance( default, type ):
        default = default()
    
    if target is None:
        return default
    
    if isinstance( target, list ):
        return cast( T, target )
    
    # TODO: PUT THIS BACK IN! Removed because for some reason we get a different class when deserialising from the IDE, but this is a problem!
    # if type(target) is not type(default):
    #     raise ValueError("Attempting to set the defaults for the value «{}», of type «{}», but the value provided, «{}», of type «{}», is not compatible with this.".format(target, type(target), default, type(default)))
    
    for k, v in default.__dict__.items():
        if k.startswith( "_" ):
            continue
        
        if k not in target.__dict__:
            target.__dict__[k] = v
    
    to_delete = []
    
    for k in target.__dict__.keys():
        if k not in default.__dict__:
            to_delete.append( k )
    
    for k in to_delete:
        del target.__dict__[k]
    
    return target


@abstract
class WriterBase:
    """
    Base class for writers.
    
    The derived class should implement:
        * (optional) A constructor
        * (optional) on_close
        * (optional) write
        * on_describe
        
    :attr extension: Extension of the file.
    :attr closed:    `True` once the file has been closed.
    """
    
    
    def __init__( self, *, extension = None ):
        """
        CONSTRUCTOR
        The derived class should pass any and all `**kwargs` to the base class.
        Other `**kwargs` may be added later.
        `*args` are not used and may be passed or not.
        :param extension: Extension of the file
        """
        self.extension = extension
        self.closed = False
    
    
    def __enter__( self ):
        return self
    
    
    def __exit__( self, exc_type, exc_val, exc_tb ):
        self.close()
    
    
    def close( self ) -> None:
        if self.closed:
            return
        
        self.on_close()
        
        self.closed = True
    
    
    def write( self, text: str ) -> None:
        self.on_write( text )
    
    
    @classmethod
    def describe( cls ) -> str:
        return cls.on_describe()
    
    
    @virtual
    def on_close( self ):
        pass
    
    
    @virtual
    def on_write( self, text: str ) -> None:
        pass
    
    
    @classmethod
    @abstract
    def on_describe( cls ) -> str:
        raise NotImplementedError( "abstract" )


@abstract
class BufferedWriter( WriterBase ):
    """
    Buffers all the output data to `self.lines` (currently just in memory).
    
    The derived class should commit the data when `on_close` is called.
    """
    
    
    def __init__( self, *args, **kwargs ) -> None:
        super().__init__( *args, **kwargs )
        self.lines = []
    
    
    @override
    def on_write( self, text: str ) -> None:
        if self.closed:
            raise ValueError( "Virtual stream has already been closed." )
        
        self.lines.append( text )
    
    
    def __repr__( self ):
        return self.__class__.__name__
    
    
    def set_extension( self, value: str ) -> None:
        pass
    
    
    @classmethod
    def on_describe( cls ) -> str:
        raise NotImplementedError( "abstract" )


class StdOutWriter( BufferedWriter ):
    """
    Dumps all the data to std-out when the stream is closed.
    """
    
    
    def on_close( self ):
        for line in self.lines:
            sys.stdout.write( line )
    
    
    @classmethod
    def on_describe( cls ) -> str:
        raise NotImplementedError( "Writes to standard output." )


class OpeningWriter( WriterBase ):
    """
    Dumps all the data to a temporary file when the stream is closed.
    Then opens the stream in the default GUI.
    The file is queued for delete when the program closes.
    """
    
    
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.file = tempfile.NamedTemporaryFile( "w", delete = False )
        self.name = self.file.name
        queue_delete( self.name )
    
    
    def on_write( self, text: str ):
        self.file.write( text )
    
    
    def on_close( self ):
        self.file.close()
        os.system( "open \"" + self.name + "\"" )
    
    
    @classmethod
    def on_describe( cls ) -> str:
        raise NotImplementedError( "Writes to a temporary file and then opens it. The file will be deleted when the application is closed.." )


class ClipboardWriter( StdOutWriter ):
    """
    Dumps all the data to the clipboard when the stream is closed.
    """
    
    
    def on_close( self ):
        import pyperclip
        pyperclip.copy( "\n".join( self.lines ) )
    
    
    @classmethod
    def on_describe( cls ) -> str:
        raise NotImplementedError( "Writes to the clipboard." )


class NowhereWriter( WriterBase ):
    """
    Doesn't write anything.
    """   
    
    @classmethod
    def on_describe( cls ) -> str:
        raise NotImplementedError( "Doesn't write anything." )


open_write_opts = { "stdout": StdOutWriter,
                    "clip"  : ClipboardWriter,
                    "null"  : NowhereWriter,
                    "open"  : OpeningWriter }


def open_write( file_name: str, extension: str = "" ) -> Union[WriterBase, TextIO]:
    """
    Opens a file for writing, accepts any of the special values in the global :variable:`open_write_opts: as the filename.
    
    :param file_name:   Name of the file. If this is `None` it is converted to `""`. This allows a default value to be added
                        to :variable:`open_write_opts`.
    :param extension:   Extension (file-type) of the file. Used by some special handlers.
    :return:            A file object or a file-like object (:class:`WriterBase`), which should have the following methods:
                            * write
                            * __enter__, __exit__, close
    """
    if file_name is None:
        file_name_lower = ""
    else:
        file_name_lower = file_name.lower()
    
    mapped: Type[BufferedWriter] = open_write_opts.get( file_name_lower )
    
    if mapped is not None:
        return mapped( extension = extension )
    
    return open( file_name, "w" )


def load_ini( file_name: str, comments: str = (";", "#", "//") ) -> Dict[str, Dict[str, str]]:
    """
    Loads an INI file.
    
    :param file_name:       File to load 
    :param comments:        Comment lines 
    :return:                INI data:
                                str - Section name ("" contains the data from any untitled section and sections with no name `[]`)
                                dict - Section data:
                                    str - Field key
                                    str - field value
    """
    r = { }
    dd = { }
    d = dd
    
    for line in open( file_name, "r" ):
        line = line.strip()
        
        if any( line.startswith( x ) for x in comments ):
            continue
        
        if line.startswith( "[" ) and line.endswith( "]" ):
            d = { }
            r[line[1:-1]] = d
        elif "=" in line:
            k, v = line.split( "=", 1 )
            d[k.strip()] = v.strip()
    
    if dd:
        if "" in r:
            dd.update( r[""] )
        
        r[""] = dd
    
    return r


class queue_delete:
    """
    The file will be deleted when the program closes.
    
    :remarks:           Class masquerading as function.
                        
                        Example usage:
                            ```
                            queue_delete( "c:\my_temporary_file.txt" )
                            ```    
    
    :data queued:       Gets the list of files to be deleted.
                        Acts to keep the references alive until the program closes.
    :attr file_name:    Name of the file
    """
    
    queued = []
    
    
    def __init__( self, file_name: str ) -> None:
        """
        CONSTRUCTOR
        Automatically adds the reference to the queue, keeping it alive
        until the program closes.
        
        :param file_name: Name of the file
        """
        self.file_name = file_name
        self.queued.append( self )
    
    
    def __del__( self ) -> None:
        """
        OVERRIDE
        On deletion, removes the file.
        """
        os.remove( self.file_name )
