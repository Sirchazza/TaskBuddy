from PySide6.QtGui import QAction
from utils import ClipboardUtils as Clip
from utils import PopupManager

class LineOperationMenu:
    """Handles the Line Operation menu creation and related functions"""
    
    def __init__(self, parent_app):
        """
        Args:
            parent_app: Reference to main app for accessing helper methods
        """
        self.app = parent_app
    
    def create_menu(self, parent_menu):

        line_menu = parent_menu.addMenu("📝 Line Operations") # Manipulate strings as a whole or on a line-by-line basis
        
        remove_breaks = QAction("Remove Line Breaks", parent_menu)
        remove_breaks.triggered.connect(self.remove_line_breaks)
        line_menu.addAction(remove_breaks)
        
        add_numbers = QAction("Add Line Numbers", parent_menu)
        add_numbers.triggered.connect(self.add_line_numbers)
        line_menu.addAction(add_numbers)
        
        trim_ws = QAction("Trim Whitespace", parent_menu)
        trim_ws.triggered.connect(self.trim_whitespace)
        line_menu.addAction(trim_ws)
        
        sort_lines = QAction("Sort Lines A-Z", parent_menu)
        sort_lines.triggered.connect(self.sort_lines)
        line_menu.addAction(sort_lines)
        
    def remove_line_breaks(self): # Move all lines in selected text to one line
        selected = Clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st!")
            return
        
        result = selected.replace('\n', ' ').replace('\r', '')
        result = ' '.join(result.split())
        Clip.paste_text(result)
    
    def trim_whitespace(self): # Trim any whitespace characters in selected text
        selected = Clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st!")
            return
        
        lines = [line.strip() for line in selected.split('\n')]
        result = '\n'.join(lines)
        Clip.paste_text(result)
    
    def add_line_numbers(self): # Add line numbers for each new line in selected text
        selected = Clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st!")
            return
        
        lines = selected.split('\n')
        numbered = '\n'.join(f"{i+1}. {line}" for i, line in enumerate(lines))
        Clip.paste_text(numbered)
    
    def sort_lines(self): # Sort lines in alphabetical or numerical order
        selected = Clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st!")
            return
        
        lines = selected.split('\n')
        sorted_lines = sorted(lines)
        result = '\n'.join(sorted_lines)
        Clip.paste_text(result)