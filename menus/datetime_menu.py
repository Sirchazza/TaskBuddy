from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from datetime import datetime
from utils import ClipboardUtils

class DateTimeMenuHandler:
    """Handles datetime menu creation and related functions"""
    
    def __init__(self, parent_app):
        """
        Args:
            parent_app: Reference to main app for accessing paste_text() and icon_cache
        """
        self.app = parent_app
        
    def create_menu(self, parent_menu):
        """Create and return the Date/Time submenu"""
        
        datetime_menu = parent_menu.addMenu("📅 Insert Date/Time") # Insert date/time in various formats
        
        datetime_iso = datetime_menu.addMenu(self.app.icon_cache.get('global', QIcon()),"ISO Format")
        self._add_format_actions(datetime_iso, parent_menu, "iso")
        
        datetime_uk = datetime_menu.addMenu(self.app.icon_cache.get('uk', QIcon()), "UK Format")
        self._add_format_actions(datetime_uk, parent_menu, "uk")
        
        datetime_usa = datetime_menu.addMenu(self.app.icon_cache.get('usa', QIcon()), "USA Format")
        self._add_format_actions(datetime_usa, parent_menu, "usa")
        
        return datetime_menu
    
    def _add_format_actions(self, submenu, parent_menu, format_type):
        """Helper to add the three standard actions for a format"""
        full_action = QAction(r"Current Date && Time", parent_menu)
        full_action.triggered.connect(lambda: self.insert_datetime(format_type))
        submenu.addAction(full_action)
        
        date_action = QAction("Date Only", parent_menu)
        date_action.triggered.connect(lambda: self.insert_date_only(format_type))
        submenu.addAction(date_action)
        
        time_action = QAction("Time Only", parent_menu)
        time_action.triggered.connect(self.insert_time_only)
        submenu.addAction(time_action)
    
    # -------- Insert date/time in various formats -------- #
    
    def insert_datetime(self, format):
        """Insert date/time in format described by menu item"""
        match format:
            case 'iso':
                text = datetime.now().strftime("%Y-%m-%d %H:%M")
            case 'uk':
                text = datetime.now().strftime("%d-%m-%Y %H:%M")
            case 'usa':
                text = datetime.now().strftime("%m-%d-%Y %H:%M")
        ClipboardUtils.paste_text(text)
    
    def insert_date_only(self, format):
        """Insert date in format described by menu item"""
        match format:
            case 'iso':
                text = datetime.now().strftime("%Y-%m-%d")
            case 'uk':
                text = datetime.now().strftime("%d-%m-%Y")
            case 'usa':
                text = datetime.now().strftime("%m-%d-%Y")
        ClipboardUtils.paste_text(text)
    
    def insert_time_only(self):
        """Insert current time"""
        text = datetime.now().strftime("%H:%M")
        ClipboardUtils.paste_text(text)