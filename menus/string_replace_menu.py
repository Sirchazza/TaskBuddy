from PySide6.QtWidgets import QInputDialog
from PySide6.QtGui import QAction
import re
from utils import ClipboardUtils as Clip
from utils import PopupManager

class StringReplaceMenu:
    """Handles String Replacement menu creation and related functions"""
    
    def __init__(self, parent_app):
        """
        Args:
            parent_app: Reference to main app for accessing helper methods
        """
        self.app = parent_app
    
    def create_menu(self, parent_menu):
        # Filename Operations submenu
        filename_menu = parent_menu.addMenu("🔄 Text Replacements") # Manipulate characters or substrings of selected text
        
        spaces_to_underscores = QAction("Spaces to Underscores", parent_menu)
        spaces_to_underscores.triggered.connect(lambda: self.replace_spaces('_'))
        filename_menu.addAction(spaces_to_underscores)
        
        spaces_to_hyphens = QAction("Spaces to Hyphens", parent_menu)
        spaces_to_hyphens.triggered.connect(lambda: self.replace_spaces('-'))
        filename_menu.addAction(spaces_to_hyphens)
        
        hyphens_to_spaces = QAction("Hyphens to Spaces", parent_menu)
        hyphens_to_spaces.triggered.connect(lambda: self.replace_character('-', ' '))
        filename_menu.addAction(hyphens_to_spaces)
        
        hyphens_to_underscores = QAction("Hyphens to Underscores", parent_menu)
        hyphens_to_underscores.triggered.connect(lambda: self.replace_character('-' ,'_'))
        filename_menu.addAction(hyphens_to_underscores)
        
        underscores_to_hyphens = QAction("Underscores to Hyphens", parent_menu)
        underscores_to_hyphens.triggered.connect(lambda: self.replace_character('_', '-'))
        filename_menu.addAction(underscores_to_hyphens)
        
        underscores_to_spaces = QAction("Underscores to Spaces", parent_menu)
        underscores_to_spaces.triggered.connect(lambda: self.replace_character('_' ,' '))
        filename_menu.addAction(underscores_to_spaces)
        
        custom_string = QAction("Custom String", parent_menu)
        custom_string.triggered.connect(lambda: self.replace_custom())
        filename_menu.addAction(custom_string)
        
    def replace_spaces(self, character): # Spaces use their own replace function to ensure all whitespace characters are replaced
        selected = Clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st!")
            return
        
        stripped = selected.strip()
        result = re.sub(r'\s+', character, stripped)
        Clip.paste_text(result)
        
    def replace_character(self, original, replacement): # Used to replace individual characters based on the menu item selected
        selected = Clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st!")
            return
        
        result = selected.replace(original, replacement)
        Clip.paste_text(result)
        
    def replace_custom(self): # replace a substring of characters with a new substring in the selected text. Replacement substring entered using pop-up window
        selected = Clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st!")
            return
        
        replacing, ok = QInputDialog.getText(None, r'Custom Character Replacement', r'Character(s) to replace:')
        if not replacing or not ok:
            return
        
        replacement, ok = QInputDialog.getText(None, 'Custom Character Replacement', 'Replacement Character(s):')
        if replacement and ok:
            result = selected.replace(replacing, replacement)
            Clip.paste_text(result)