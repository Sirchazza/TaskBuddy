from PySide6.QtGui import QAction
from utils import ClipboardUtils as clip
from utils import PopupManager

class SQLMenu:
    """Handles the SQL code menu creation and related functions"""
    
    def __init__(self, parent_app):
        """
        Args:
            parent_app: Reference to main app for accessing helper methods
        """
        self.app = parent_app
    
    def create_menu(self, parent_menu):
        
        SQL_menu = parent_menu.addMenu("🛢 SQL Functions") # SQL based utilities
        
        old_trim = QAction("Wrap Text With L/R Trim", parent_menu)
        old_trim.triggered.connect(lambda: self.trim_text(0))
        SQL_menu.addAction(old_trim)
        
        new_trim = QAction("Wrap Text With Trim", parent_menu)
        new_trim.triggered.connect(lambda: self.trim_text(1))
        SQL_menu.addAction(new_trim)
        
        all_commas_first = QAction("Move Commas To Front (All)", parent_menu)
        all_commas_first.triggered.connect(lambda: self.commas_first(1))
        SQL_menu.addAction(all_commas_first)
        
        exc_commas_first = QAction("Move Commas To Front (exc. 1st)", parent_menu)
        exc_commas_first.triggered.connect(lambda: self.commas_first(0))
        SQL_menu.addAction(exc_commas_first)
        
        excel_to_sql_columns = QAction("Excel Columns to Python", parent_menu)
        excel_to_sql_columns.triggered.connect(self.excel_to_sql_cols)
        SQL_menu.addAction(excel_to_sql_columns)
        
        remove_sq_brackets = QAction("Remove Square Brackets", parent_menu)
        remove_sq_brackets.triggered.connect(self.remove_square_brackets)
        SQL_menu.addAction(remove_sq_brackets)
        
    def trim_text(self, type): # Wrap text with TRIM function. 0 = L&R Trim (Old Format), 1 = TRIM (New Format)
        selected = clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st!")
            return
        
        if type == 0:
            result = fr"LTRIM(RTRIM({selected}))"
        else:
            result = fr"TRIM({selected})"
        
        clip.paste_text(result)

    def commas_first(self, inc_top_line): # Move commas from the end of a line to the front.
        # If inc_top_line = 0 then the comma is removed from the end of the 1st line but not added to the front of the line. 
        selected = clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st!")
            return
        
        lines = selected.split('\n')
        
        if inc_top_line == 1:
            for i, line in enumerate(lines):
                clean = line.rstrip()
                text_only = clean.lstrip()
                if clean.endswith(','):
                    whitespace_count = len(clean) - len(text_only)
                    lines[i] = f"{clean[:whitespace_count]},{clean[whitespace_count:-1]}"
                elif not text_only.startswith(','):
                    lines[i] = f"{clean[:whitespace_count]},{clean[whitespace_count:]}"
                else:
                    pass
        else:
            top_line = lines[0].rstrip()
            if top_line.endswith(','):
                lines[0] = top_line[:-1]
            for i, line in enumerate(lines[1:], 1):
                clean = line.rstrip()
                text_only = clean.lstrip()
                if clean.endswith(','):
                    whitespace_count = len(clean) - len(text_only)
                    lines[i] = f"{clean[:whitespace_count]},{clean[whitespace_count:-1]}"
                elif not text_only.startswith(','):
                    lines[i] = f"{clean[:whitespace_count]},{clean[whitespace_count:]}"
                else:
                    pass
                
        result = '\n'.join(lines)
        clip.paste_text(result)
        
    def excel_to_sql_cols(self):
        selected = clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st!")
            return
        
        lines = selected.split('\t')
        
        top_line = lines[0].strip()
        lines[0] = f"\t{top_line}"
        
        for i, line in enumerate(lines[1:], 1):
                clean_line = line.strip()
                lines[i] = f"\t, {clean_line}"
                
        result = '\n'.join(lines)
        clip.paste_text(result)
        
    def remove_square_brackets(self):
        selected = clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st!")
            return
        
        lines = selected.split('\n')
        
        for i, line in enumerate(lines, 0):
                scrubbed = line.replace('[', '').replace(']', '')
                lines[i] = scrubbed
                
        result = '\n'.join(lines)
        clip.paste_text(result)
        