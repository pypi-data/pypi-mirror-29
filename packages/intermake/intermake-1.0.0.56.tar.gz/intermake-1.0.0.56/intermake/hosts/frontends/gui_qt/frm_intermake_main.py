"""
Main window for GUI
"""

from typing import cast

from PyQt5.QtCore import QMargins, Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QMainWindow, QMessageBox, QSplitter, QTextEdit, QTreeWidget, QVBoxLayout, QWidget
from intermake.hosts.frontends.gui_qt.designer.resource_files import resources_rc
from intermake.hosts.frontends.gui_qt.designer.frm_intermake_main_designer import Ui_MainWindow

from intermake.engine.async_result import AsyncResult
from intermake.engine.environment import MENV
from intermake.hosts.frontends.gui_qt.views.results_view import ResultsView
from intermake.hosts.gui import IGuiPluginHostWindow
from intermake.visualisables.visualisable import EIterVis
from mhelper_qt.qt_gui_helper import exqtSlot


cast( None, resources_rc )

__author__ = "Martin Rusilowicz"


class FrmIntermakeMain( QMainWindow, IGuiPluginHostWindow ):
    """
    Main window
    """
    
    
    def __init__( self, can_return_to_cli: bool ):
        """
        CONSTRUCTOR
        """
        # ...QT stuff
        QMainWindow.__init__( self )
        self.ui = Ui_MainWindow()
        self.ui.setupUi( self )
        
        self.__ever_in_cli = can_return_to_cli
        self.__return_to_console = False
        
        env = MENV
        
        # ...UI stuff
        self.setWindowTitle( env.name + " " + env.version )
        
        self.views = []
        
        for sub_object in env.root.visualisable_info().iter_children( EIterVis.CONTENTS | EIterVis.PROPERTIES ):
            # Create tab page
            tab_page = QWidget()
            
            # Set vertical layout
            tab_page_layout = QVBoxLayout()
            tab_page.setLayout( tab_page_layout )
            
            # Create "toolbar"
            frame = QFrame()
            tab_page_layout.addWidget( frame )
            
            # Create "toolbar" layout
            frame_layout = QHBoxLayout()
            frame_layout.setContentsMargins( QMargins( 0, 0, 0, 0 ) )
            frame.setLayout( frame_layout )
            
            # Create splitter
            splitter = QSplitter()
            splitter.setOrientation( Qt.Vertical )
            tab_page_layout.addWidget( splitter )
            
            # Create tree
            tree_widget = QTreeWidget( splitter )
            
            # Create text editor
            text_edit = QTextEdit( splitter )
            
            # Create view
            value = sub_object
            view = ResultsView( widget = tree_widget,
                                text_widget = text_edit,
                                toolbar_layout = frame_layout,
                                on_get_source = (lambda closure: lambda: closure)( value ) )
            self.views.append( view )
            
            self.ui.TAB_MAIN.addTab( tab_page, sub_object.key )
        
        # ...defaults
        self.ui.TAB_MAIN.setCurrentIndex( 0 )
    
    
    # ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    # ▒ BUTTON CLICKS ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    # ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    
    def closeEvent( self, event: QCloseEvent ):
        if self.__ever_in_cli:
            q = QMessageBox.question( self, "Close", "You have closed the GUI. Do you wish to return to the CLI?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel )
            
            if q == QMessageBox.Cancel:
                event.ignore()
                return
            elif q == QMessageBox.Yes:
                self.__return_to_console = True
            else:
                self.__return_to_console = False
    
    
    @exqtSlot()
    def on_ACTION_HELP_ABOUT_triggered( self ) -> None:
        """
        Signal handler: Help -> About
        """
        msg = QMessageBox( self )
        msg.setIcon( QMessageBox.Information )
        msg.setText( "fasta.explorer" )
        msg.setInformativeText( "Version 1" )
        msg.exec_()
    
    
    @exqtSlot()
    def on_ACTION_CONFIGURATION_triggered( self ) -> None:
        """
        Signal handler:
        """
        pass
    
    
    def plugin_completed( self, result: AsyncResult ):
        """
        A plugin has finished - results have been received!
        """
        self.statusBar().showMessage( "(PLUGIN COMPLETED) " + str( result ) )

    def return_to_console( self ):
        return self.__return_to_console