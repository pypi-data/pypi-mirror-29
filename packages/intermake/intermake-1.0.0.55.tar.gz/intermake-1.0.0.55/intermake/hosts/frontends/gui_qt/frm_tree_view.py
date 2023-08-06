from typing import Optional, Callable

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QTreeWidgetItem

from intermake.engine.environment import MENV
from intermake.hosts.frontends.gui_qt.designer.frm_tree_view_designer import Ui_Dialog

from intermake.hosts.frontends.gui_qt import intermake_gui
from intermake.hosts.frontends.gui_qt.views.results_view import ResultsView
from intermake.visualisables.visualisable import UiInfoProperty
from intermake.visualisables.visualisable_operations import PathToVisualisable


class FrmTreeView( QDialog ):
    def __init__( self,
                  parent: QDialog,
                  message: str,
                  root: UiInfoProperty,
                  on_selecting: Optional[Callable[[UiInfoProperty], bool]] ):
        """
        CONSTRUCTOR
        """
        QDialog.__init__( self, parent )
        self.ui = Ui_Dialog( self )
        
        self.ui.LBL_MAIN.setText( str( message ) )
        self.__results = ResultsView( widget = self.ui.TVW_MAIN,
                                      text_widget = self.ui.TXT_MAIN, 
                                      toolbar_layout = self.ui.HOZ_TOOLBAR,
                                      on_get_source = lambda: root,
                                      on_selected = self.__on_selected,
                                      on_selecting = on_selecting )
        self.__acceptability = on_selecting
        self.__result: PathToVisualisable = None
        self.on_TVW_MAIN_itemSelectionChanged()
    
    
    def __on_selected( self, item: QTreeWidgetItem ) -> None:
        self.__accept( item )
    
    
    @staticmethod
    def request( parent: QDialog,
                 message: str,
                 root: Optional[UiInfoProperty] = None,
                 on_selecting: Optional[Callable[[UiInfoProperty], bool]] = None ) -> Optional[PathToVisualisable]:
        if root is None:
            root = UiInfoProperty( MENV.root.visualisable_info().name, MENV.root )
        
        if message is None:
            message = "Select object"
        
        frm = FrmTreeView( parent, message, root, on_selecting )
        
        if frm.exec_():
            return frm.__result
        
        return None
    
    
    @pyqtSlot()
    def on_TVW_MAIN_itemSelectionChanged( self ) -> None: #TODO: BAD_HANDLER - The widget 'TVW_MAIN' does not appear in the designer file.
        data = self.__results.selected_data()
        
        box = self.ui.BTNBOX_MAIN  # type: QDialogButtonBox
        
        if data is not None:
            box.button( QDialogButtonBox.Ok ).setEnabled( self.__acceptability( data ) )
        else:
            box.button( QDialogButtonBox.Ok ).setEnabled( False )
    
    
    @pyqtSlot()
    def on_BTNBOX_MAIN_accepted( self ) -> None:
        """
        Signal handler:
        """
        self.__accept( self.__results.selected_item() )
    
    
    def __accept( self, item: QTreeWidgetItem ):
        path = self.__results.data_path( item )
        
        if path is not None and self.__acceptability( path[-1] ):
            self.__result = PathToVisualisable( path )
            self.accept()
    
    
    @pyqtSlot()
    def on_BTNBOX_MAIN_rejected( self ) -> None:
        """
        Signal handler:
        """
        self.reject()
