import sys
import os
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from PySide6.QtGui import QIcon, QAction, QCursor, QFontMetrics, QPixmap
from PySide6.QtCore import Qt, QObject, Signal, QThread
import keyboard as kb
from menus import DateTimeMenuHandler, FileOperationsMenuHandler, CaseMenuHandler, StringReplaceMenu, LineOperationMenu, SQLMenu, BrowserMenu, SnippetsMenu
from utils import ReadmeViewer


def get_resource_path(relative_path):
    """Get absolute path to resource"""
    if getattr(sys, 'frozen', False):
        # Running as compiled EXE
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class MenuTrigger(QObject):
    """Helper class to emit signal from keyboard thread"""
    show_menu = Signal()

class TextToolsApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        self.icon_cache = {}
        self.preload_resources()
        
        self.menu_trigger = MenuTrigger()
        self.menu_trigger.show_menu.connect(self.show_menu)
        
        self.current_menu = None  # Track active menu
        self.hotkey_paused = False
        
        self.datetime_handler = DateTimeMenuHandler(self)
        self.case_handler = CaseMenuHandler(self)
        self.string_rep_handler = StringReplaceMenu(self)
        self.line_ops_handler = LineOperationMenu(self)
        self.sql_handler = SQLMenu(self)
        self.file_ops_handler = FileOperationsMenuHandler(self)
        self.browser_handler = BrowserMenu(self)
        self.snippets_handler = SnippetsMenu(self)
        
        self.readme_window = None
        
        self.setup_tray_icon()
        self.setup_hotkey()
        
    def preload_resources(self):
        """Pre-load icons and initialize Qt components to reduce first-menu delay"""
        # Create a dummy menu to initialize Qt's menu system
        dummy_menu = QMenu()
        dummy_font_metrics = QFontMetrics(dummy_menu.font())
        icon_size = dummy_font_metrics.height()
        
        icon_mapping = {
            'global': get_resource_path('icons/globe.ico'),
            'icon': get_resource_path('icons/ico.ico'),
            'uk': get_resource_path('icons/uk_flag.ico'),
            'usa': get_resource_path('icons/usa_flag.ico'),
            'google': get_resource_path('icons/google.ico'),
            'chrome': get_resource_path('icons/chrome.ico'),
            'snow': get_resource_path('icons/snow_logo.ico'),
            'favicon': get_resource_path('icons/task_buddy_blue.ico'),
            'favicon_paused': get_resource_path('icons/task_buddy_red.ico'),
            'word': get_resource_path('icons/word_icon.ico'),
            'project': get_resource_path('icons/project.ico'),
            'zip_folder': get_resource_path('icons/zip_folder.ico'),
            'picture': get_resource_path('icons/picture.ico')
        }
        
        for name, path in icon_mapping.items():
            if os.path.exists(path):
                pixmap = QPixmap(path)
                scaled_pixmap = pixmap.scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.icon_cache[name] = QIcon(scaled_pixmap)
        
        # Delete dummy menu
        dummy_menu.deleteLater()
        
    def setup_hotkey(self):
        """Setup global hotkey listener with suppression"""
        # Numpad decimal point
        kb.add_hotkey('alt+shift+decimal', 
                    lambda: self.menu_trigger.show_menu.emit(),
                    suppress=True)
        
                # Case conversion hotkeys
        kb.add_hotkey('alt+shift+u', 
                    lambda: self.case_handler.convert_case("upper"),
                    suppress=True)
        
        kb.add_hotkey('alt+shift+l', 
                    lambda: self.case_handler.convert_case("lower"),
                    suppress=True)
        
        kb.add_hotkey('alt+shift+t', 
                    lambda: self.case_handler.convert_case("title"),
                    suppress=True)
        
        kb.add_hotkey('alt+shift+s', 
                    lambda: self.case_handler.convert_case("sentence"),
                    suppress=True)
        
        print("Hotkey listener started - Press Alt+Shift+. (numpad)")
    
    def toggle_hotkey(self):
        """Pause or unpause the hotkey listener"""
        if self.hotkey_paused:
            # Unpause - re-enable the hotkey
            self.setup_hotkey()
            self.hotkey_paused = False
            print("Hotkey listener resumed")
        else:
            # Pause - remove the hotkey
            kb.unhook_all()
            self.hotkey_paused = True
            print("Hotkey listener paused")
        
        # Update both icon and menu
        self.update_tray_icon()
        self.update_tray_menu()
        
        # Update the tray menu to reflect the new state
        self.update_tray_menu()
    
    def update_tray_menu(self):
        """Update the tray menu to show current hotkey state"""
        tray_menu = QMenu()
        
        open_action = QAction("Open Menu (Alt+Shift+.)", self.app)
        open_action.triggered.connect(self.show_menu)
        open_action.setEnabled(not self.hotkey_paused)  # Disable if paused
        tray_menu.addAction(open_action)
        
        tray_menu.addSeparator()
        
        readme_action = QAction("View User Guide", self.app)
        readme_action.triggered.connect(self.show_readme)
        tray_menu.addAction(readme_action)
        
        tray_menu.addSeparator()
        
        # Toggle action with dynamic text
        toggle_text = "Resume Hotkey" if self.hotkey_paused else "Pause Hotkey"
        toggle_action = QAction(toggle_text, self.app)
        toggle_action.triggered.connect(self.toggle_hotkey)
        tray_menu.addAction(toggle_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("Exit", self.app)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray.setContextMenu(tray_menu)
    
    def show_readme(self):
        """Show or focus the README window"""
        if self.readme_window is None or not self.readme_window.isVisible():
            self.readme_window = ReadmeViewer(
                html_file='README.html',
                title='Task Buddy - User Guide',
                window_icon='icons/favicon.ico',
                image_folder='icons'
            )
            self.readme_window.show()
        else:
            # Window already open - bring to front
            self.readme_window.raise_()
            self.readme_window.activateWindow()
    
    def update_tray_icon(self):
        """Update tray icon based on hotkey state"""
        if self.hotkey_paused:
            icon_key = 'favicon_paused'  # Or use a different icon from your resources
            tooltip = "Text Tools - Hotkey Paused"
        else:
            icon_key = 'favicon'
            tooltip = "Text Tools - Alt+Shift+. (numpad) - Active"
        
        icon = self.icon_cache.get(icon_key, self.icon_cache.get('favicon', QIcon()))
        self.tray.setIcon(icon)
        self.tray.setToolTip(tooltip)
    
    def setup_tray_icon(self):
        """Create system tray icon"""
        self.tray = QSystemTrayIcon()
        
        try:
            icon = self.icon_cache.get('favicon', QIcon())
        except:  # noqa: E722
            icon = QIcon.fromTheme("text-x-generic")
        self.tray.setIcon(icon)
        self.tray.setToolTip("Text Tools - Alt+Shift+. (numpad)")
        
        # Initialize the tray menu
        self.update_tray_menu()
        
        self.tray.show()
        
        print("System tray icon created")
    
    def show_menu(self):
        """Show native context menu at cursor"""
        print(f"show_menu called on thread: {QThread.currentThread()}")  # Debug
        
        menu = QMenu()
        menu.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)  # This should handle click-outside
        menu.setAttribute(Qt.WA_DeleteOnClose)
        menu.setStyleSheet("""
            QMenu {
                background-color: palette(base);
                border: 1px solid palette(shadow);
            }
            QMenu::item {
                padding: 5px 30px 5px 20px;
                border: 1px solid transparent;
            }
            QMenu::item:selected {
                background-color: palette(highlight);
                color: palette(highlighted-text);
            }
            QMenu::separator {
                height: 1px;
                background: palette(mid);
                margin: 5px 0px;
            }
            QMenu::icon {
            padding-left: 0px;
            padding-right: 2px;  /* Reduce gap between icon and text */
            }
        """)
        self.datetime_handler.create_menu(menu)
        self.case_handler.create_menu(menu)
        self.string_rep_handler.create_menu(menu)
        self.line_ops_handler.create_menu(menu)
        self.snippets_handler.create_menu(menu)
        self.sql_handler.create_menu(menu)
        self.browser_handler.create_menu(menu)
        self.file_ops_handler.create_menu(menu)
        
# Show menu at cursor position
        cursor_pos = QCursor.pos()
        print(f"Showing menu at {cursor_pos}")
        menu.exec(cursor_pos)
        print("Menu closed")
        
    def quit_app(self):
        """Clean shutdown"""
        print("Shutting down...")
        kb.unhook_all()  # Clean up keyboard hooks
        self.tray.hide()
        self.app.quit()
    
    def run(self):
        """Run the application"""
        print("Text Tools running... Press Alt+Shift+. (numpad) to open menu")
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = TextToolsApp()
    app.run()