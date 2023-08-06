from cmath import rect

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QMenu, QWidget, QMenuBar, QMainWindow


def show( control: QWidget, *args ) -> object:
    menu = QMenu()
    
    if control.window().styleSheet():
        menu.setStyleSheet( control.window().styleSheet() )
    
    r = []
    
    for arg in args:
        r.append( menu.addAction( str( arg ) ) )
    
    selected = menu.exec_( control.mapToGlobal( QPoint( 0, control.height() ) ) )
    
    if selected is None:
        return None
    
    return args[r.index( selected )]


def show_menu( control, menu ):
    return menu.exec_( control.sender().mapToGlobal( QPoint( 0, control.sender().height() ) ) )


def drop_menu( control, menu: QMenu ):
    menu_bar = control.parent().menuBar()
    p = menu_bar.mapToGlobal(menu_bar.rect().bottomLeft())
    return menu.exec_( p )
