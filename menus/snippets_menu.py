from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QInputDialog
from utils import ClipboardUtils as clip
import tomllib

class SnippetsMenu:
    """Handles the Snippets menu creation and related functions"""
    
    def __init__(self, parent_app):
        """
        Args:
            parent_app: Reference to main app for accessing helper methods
        """
        self.app = parent_app
        self.snippets = self.load_snippets()
    
    def load_snippets(self):
        """Load snippets from TOML file, create sample file if not found"""
        try:            
            with open("snippets.toml", "rb") as f:
                return tomllib.load(f)
        except FileNotFoundError:
            print("snippets.toml not found, creating sample file")
            sample_content = """# Snippets Configuration File

["Example/Hello World"]
text = "Hello, {name}!"
params = ["name"]

["Example/Simple Text"]
text = "This is a simple snippet with no parameters."

"""
            with open("snippets.toml", "w", encoding="utf-8") as f:
                f.write(sample_content)
            
            # Load the newly created file
            with open("snippets.toml", "rb") as f:
                return tomllib.load(f)
        except Exception as e:
            print(f"Error loading snippets: {e}")
            return {}
    
    def create_menu(self, parent_menu):
        """Create snippets menu with submenus from TOML file"""
        snippets_menu = parent_menu.addMenu("📝 Snippets")
        
        # Group by category
        categories = {}
        for full_path, template_data in self.snippets.items():
            if '/' in full_path:
                category, action_name = full_path.split('/', 1)
            else:
                category = "Other"
                action_name = full_path
            
            if category not in categories:
                categories[category] = {}
            categories[category][action_name] = template_data
        
        # Create submenus
        for category_name, actions in sorted(categories.items()):
            submenu = QMenu(category_name, snippets_menu)
            snippets_menu.addMenu(submenu)
            
            for action_name, template_data in sorted(actions.items()):
                action = QAction(action_name, submenu)
                action.triggered.connect(lambda checked=False, td=template_data: self.handle_snippet(td))
                submenu.addAction(action)

    def handle_snippet(self, template_data):
        """Handle template with optional parameters"""
        text = template_data.get('text', '')
        params = template_data.get('params', [])
        
        if params:
            values = {}
            for param in params:
                # Convert snake_case to Title Case for display
                display_name = param.replace('_', ' ').title()
                input_text, ok = QInputDialog.getText(None, "Input Required", f"Enter {display_name}:")
                if not ok:
                    return  # User cancelled
                values[param] = input_text
            
            result = text.format(**values)
        else:
            result = text
        
        if result:
            clip.paste_text(result)