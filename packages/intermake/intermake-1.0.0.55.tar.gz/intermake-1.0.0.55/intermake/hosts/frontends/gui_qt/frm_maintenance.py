from typing import cast

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QAction, QDialog, QMenu, QWidget
from intermake.hosts.frontends.gui_qt.designer.resource_files import resources_rc
from intermake.hosts.frontends.gui_qt.designer.frm_maintenance_designer import Ui_Dialog

from intermake.engine.async_result import AsyncResult
from intermake.engine.constants import EDisplay, EStream
from intermake.engine.environment import MENV
from intermake.engine.progress_reporter import UpdateInfo
from intermake.hosts.frontends.gui_qt import intermake_gui
from intermake.hosts.frontends.gui_qt.views.progress_view import ProgressView
from mhelper_qt import qt_gui_helper
from mhelper_qt.qt_gui_helper import exqtSlot


__author__ = "Martin Rusilowicz"

cast( None, resources_rc )


class FrmMaintenance( QDialog ):
    """
    This is the form that shows when a plugin is running.
    """
    
    
    def __init__( self, parent: QWidget, title: str ):
        """
        CONSTRUCTOR
        """
        from intermake.hosts.gui import GuiHost
        
        QDialog.__init__( self, parent )
        self.ui = Ui_Dialog( self )
        
        # Set our properties
        host = cast( GuiHost, MENV.host )
        self.__was_cancelled = False
        self.__auto_close = host.gui_settings.gui_auto_close_progress
        self.__autoscroll = host.gui_settings.gui_auto_scroll_progress
        self.__finished = False
        self.__log_view = ProgressView( self.ui.TVW_LOG )
        self.__log_view.set_auto_scroll( self.__autoscroll )
        self.__display = host.gui_settings.gui_progress_display
        self.__needs_raise = True
        self.__maximise_progress = False
        self.__maximise_output = False
        self.__has_text_messages = False
        
        # Set the default view to the simple one
        self.setWindowTitle( title )
        self.setWindowFlags( Qt.Dialog | Qt.Desktop )
        self.__update_show_details()
        self.ui.TXT_TITLE.setText( title )
        self.ui.BTN_SHOW_PROGRESS.setChecked( True )
        self.on_BTN_SHOW_PROGRESS_clicked()
        self.ui.BTN_CLOSE.setVisible( False )
    
    
    def __update_show_details( self ):
        self.ui.BTN_SHOW_OUTPUT.setChecked( self.__maximise_output )
        self.ui.BTN_SHOW_PROGRESS.setChecked( self.__maximise_progress )
        self.ui.FRA_PROGRESS.setVisible( not self.__maximise_output )
        self.ui.FRA_MESSAGES.setVisible( not self.__maximise_progress )
    
    
    # region ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ EXTERNAL COMMANDS ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    
    def worker_update( self, info: UpdateInfo ):
        if info.message:
            self.__add_message_to_textbox( info.message, info.stream )
        else:
            self.__add_progress_to_progress_list( info )
        
        if self.__needs_raise:
            self.activateWindow()
            self.raise_()
            self.__needs_raise = False
    
    
    def was_cancelled( self ) -> bool:
        return self.__was_cancelled
    
    
    def worker_finished( self, result: AsyncResult ):
        self.__finished = True
        
        # Tag the messages onto the result
        result.ex_messages_html = self.ui.TXT_MESSAGES.toHtml()
        
        if self.__auto_close:
            self.close()
        else:
            self.__log_view.add_comment( "All done.", "You may now close the dialogue" )
            self.__add_message_to_textbox( "All done. You may now close the dialogue.", EStream.PROGRESS )
            self.ui.BTN_CANCEL.setVisible( False )
            self.ui.BTN_CLOSE.setVisible( True )
    
    
    # endregion
    
    
    def __add_progress_to_progress_list( self, info ):
        """
        Adds a progress message to the progress list.
        """
        self.__log_view.add( info )
    
    
    def __add_message_to_textbox( self, message_text: str, message_stream: EStream ):
        """
        Adds a message to the textbox.
        """
        html = qt_gui_helper.ansi_to_html( message_text )
        self.ui.TXT_MESSAGES.append( html )
        
        if not self.__has_text_messages and message_stream not in (EStream.PROGRESS, EStream.EXTERNAL_STDERR, EStream.EXTERNAL_STDOUT, EStream.ECHO, EStream.SYSTEM):
            self.__has_text_messages = True
            self.__maximise_progress = False
            self.__maximise_output = True
            self.__auto_close = False
            self.__update_show_details()
    
    
    def closeEvent( self, event: QCloseEvent ):
        if not self.__finished:
            event.ignore()
    
    
    @exqtSlot()
    def on_BTN_CANCEL_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__log_view.add_comment( "~~ Cancel requested ~~", "The process will stop during the next iteration" )
        self.ui.BTN_CANCEL.setVisible( False )
        self.__was_cancelled = True
    
    
    @exqtSlot()
    def on_BTN_CLOSE_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.close()
    
    
    @exqtSlot()
    def on_BTN_ESTIMATE_clicked( self ) -> None:
        """
        Signal handler:
        """
        menu = QMenu()
        
        __mnu_autoscroll: QAction = menu.addAction( "Auto-scroll to new entries" )
        __mnu_autoscroll.setCheckable( True )
        __mnu_autoscroll.setChecked( self.__autoscroll )
        
        __mnu_autoclose: QAction = menu.addAction( "Auto-close when complete" + (" (next time)" if self.__finished else "") )
        __mnu_autoscroll.setCheckable( True )
        __mnu_autoclose.setChecked( self.__auto_close )
        
        submenu: QAction = menu.addMenu( "Display details" )
        
        __mnu_progress: QAction = submenu.addAction( "Progress" )
        __mnu_progress.setCheckable( True )
        __mnu_progress.setChecked( self.__maximise_progress )
        
        __mnu_messages: QAction = submenu.addAction( "Messages" )
        __mnu_messages.setCheckable( True )
        __mnu_messages.setChecked( self.__maximise_output )
        
        __mnu_both: QAction = submenu.addAction( "Both" )
        __mnu_both.setCheckable( True )
        __mnu_both.setChecked( not self.__maximise_progress and not self.__maximise_output )
        
        submenu: QAction = menu.addMenu( "Display progress as" )
        
        options = { }
        
        for option in EDisplay:
            action: QAction = submenu.addAction( MENV.host.translate_name( option.name.lower() ) )
            action.setCheckable( True )
            action.setChecked( option == self.__display )
            options[action] = option
        
        selected = menu.exec_( self.ui.BTN_ESTIMATE.mapToGlobal( QPoint( 0, self.ui.BTN_ESTIMATE.height() ) ) )
        
        if selected is __mnu_autoscroll:
            self.__autoscroll = not self.__autoscroll
            self.__log_view.set_auto_scroll( self.__autoscroll )
        elif selected is __mnu_autoclose:
            self.__auto_close = not self.__auto_close
        elif selected is __mnu_progress:
            self.__maximise_progress = True
            self.__maximise_output = False
            self.__update_show_details()
        elif selected is __mnu_messages:
            self.__maximise_progress = False
            self.__maximise_output = True
            self.__update_show_details()
        elif selected is __mnu_both:
            self.__maximise_progress = False
            self.__maximise_output = False
            self.__update_show_details()
        elif selected is not None:
            self.__display = options[selected]
    
    
    @exqtSlot()
    def on_BTN_SHOW_OUTPUT_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__maximise_output = self.ui.BTN_SHOW_OUTPUT.isChecked()
        self.__update_show_details()
    
    
    @exqtSlot()
    def on_BTN_SHOW_PROGRESS_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__maximise_progress = self.ui.BTN_SHOW_PROGRESS.isChecked()
        self.__update_show_details()
