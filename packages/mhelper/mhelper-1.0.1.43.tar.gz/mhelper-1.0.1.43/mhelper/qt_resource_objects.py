__author__ = "Martin Rusilowicz"


class ResourceIcon:
    def __init__( self, path: str ):
        self._path = path
        self._icon = None
    
    
    def __repr__( self ):
        return "ResourceIcon(«{0}»)".format( self._path )
    
    
    def __call__( self, *args, **kwargs ):
        return self.icon()
    
    
    def icon( self ):
        from PyQt5.QtGui import QIcon
        
        if not self._icon:
            self._icon = QIcon( self._path )
        
        return self._icon
