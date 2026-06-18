import time
import pyperclip
import keyboard as kb
import win32gui
import win32com.client
from pathlib import Path
from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt

# -------- Clipboard methods -------- #

class ClipboardUtils:
    
    @staticmethod
    def get_selected_text(): # Copies the selected text for string manipulation
        """Get currently selected text via clipboard"""
        old_clipboard = pyperclip.paste()
        pyperclip.copy('')
        
        # Use keyboard library for key simulation
        kb.send('ctrl+c')
        time.sleep(0.1)
        
        selected = pyperclip.paste()
        
        if not selected:
            pyperclip.copy(old_clipboard)
            return None
        
        return selected

    @staticmethod
    def paste_text(text): # Replace text after manipulation
        """Paste text at cursor position"""
        pyperclip.copy(text)
        kb.send('ctrl+v')
        

# -------- File Explorer Methods -------- #

def _get_selected_file(window, amount):
    selected = window.Document.SelectedItems()
    if selected.Count > 0:
        if amount == "single":
            return selected.Item(0).Path
        else:
            paths = []
            for i in range(selected.Count):
                paths.append(selected.Item(i).Path)
            return paths
    else:
        return None
    
class FileExplorerUtils:
    
    @staticmethod
    def get_explorer_selection(amount="single"):
        import traceback
        
        hwnd = win32gui.GetForegroundWindow()
        
        try:
            shell = win32com.client.Dispatch("Shell.Application")
        except Exception as e:
            print(f"Failed to create Shell.Application: {e}")
            return None
        
        try:
            windows_list = list(shell.Windows())
        except Exception as e:
            return None
        
        # First loop - try to match foreground window
        for i, window in enumerate(windows_list):
            full_name = window.FullName
            window_hwnd = window.HWND
            
            if "explorer.exe" in full_name.lower():
                if window_hwnd == hwnd:
                    result = _get_selected_file(window, amount)
                    return result
        
        # Second loop - fallback to any explorer window
        for i, window in enumerate(windows_list):
            full_name = window.FullName
            if "explorer.exe" in full_name.lower():
                result = _get_selected_file(window, amount)
                if not result:
                    continue
                button = PopupManager.question(
                    "Project File Conversion",
                    f"Convert {result} to an Excel file?",
                )
                if button == QMessageBox.No:
                    continue
                return result
        
        return None
    
    @staticmethod
    def get_folder_path(selected_file, title="Select Output Folder"):
        filepath = Path(selected_file)
        start_dir = filepath.parent if filepath.is_file() else filepath
        folder_path = QFileDialog.getExistingDirectory(
            None,
            title,
            str(start_dir),
            QFileDialog.Option.ShowDirsOnly
        )
        return Path(folder_path) if folder_path else None


class ProgressBar:
    def __init__(self, title="Processing", message="Please wait...", maximum=100, parent=None):
        self.app = QApplication.instance()
        
        # Create widget instead of dialog
        self.window = QWidget()
        self.window.setWindowTitle(title)
        self.window.setMinimumSize(250, 120)
        self.window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        
        layout = QVBoxLayout()
        
        self.label = QLabel(message)
        layout.addWidget(self.label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        self.window.setLayout(layout)
        
    def __enter__(self):
        """Context manager entry - automatically shows dialog"""
        self.show()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - automatically closes dialog"""
        self.close()
        return False
        
    def show(self):
        self.window.show()
        self.app.processEvents()
    
    def increment(self, message=None):
        current = self.progress_bar.value()
        self.update(current + 1, message)
    
    def update(self, value, message=None):
        self.progress_bar.setValue(value)
        if message:
            self.label.setText(message)
        self.app.processEvents()
        
    def max(self, value):
        self.progress_bar.setMaximum(value)
    
    def close(self):
        self.window.close()
        
class PopupManager:
    
    @staticmethod
    def info(title: str, message: str, parent: QWidget | None = None):
        return QMessageBox.information(parent, title, message)
        
    @staticmethod
    def warning(title: str, message: str, parent: QWidget | None = None):
        return QMessageBox.warning(parent, title, message)
        
    @staticmethod
    def question (title: str, message: str, parent: QWidget | None = None):
        return QMessageBox.question(parent, title, message)
        
    @staticmethod
    def about (title: str, message: str, parent: QWidget | None = None):
        return QMessageBox.about(parent, title, message)
        
    @staticmethod
    def critical (title: str, message: str, parent: QWidget | None = None):
        return QMessageBox.critical(parent, title, message)
