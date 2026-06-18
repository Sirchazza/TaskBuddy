# Change Case submenu
from PySide6.QtGui import QAction
from utils import ClipboardUtils as Clip
from utils import PopupManager


class CaseMenuHandler:
    """Handles Case menu creation and related functions"""
    
    def __init__(self, parent_app):
        """
        Args:
            parent_app: Reference to main app for accessing helper methods
        """
        self.app = parent_app
    
    def create_menu(self, parent_menu):
        case_menu = parent_menu.addMenu("🔤 Change Case") # Specific case switching utilities for the selected text
        
        case_upper = QAction("UPPERCASE", parent_menu)
        case_upper.triggered.connect(lambda: self.convert_case("upper"))
        case_menu.addAction(case_upper)
        
        case_lower = QAction("lowercase", parent_menu)
        case_lower.triggered.connect(lambda: self.convert_case("lower"))
        case_menu.addAction(case_lower)
        
        case_title = QAction("Title Case", parent_menu)
        case_title.triggered.connect(lambda: self.convert_case("title"))
        case_menu.addAction(case_title)
        
        case_sentence = QAction("Sentence case", parent_menu)
        case_sentence.triggered.connect(lambda: self.convert_case("sentence"))
        case_menu.addAction(case_sentence)
        
    def convert_case(self, mode): # Convert selected text to case based on menu item selected
        selected = Clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st for me to change it's case!")
            return
        
        match mode:
            case "upper":
                result = selected.upper()
            case "lower":
                result = selected.lower()
            case "title":
                result = selected.title()
            case "sentence":
                result = selected.capitalize()
        
        Clip.paste_text(result)