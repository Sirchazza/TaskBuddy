import sys
import os
import base64
from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QTextBrowser, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

def get_resource_path(relative_path):
    """Get absolute path to resource - works for both dev and PyInstaller"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def get_image_as_base64(image_path):
    """Convert image to base64 data URI for embedding in HTML"""
    full_path = get_resource_path(image_path)
    
    if not os.path.exists(full_path):
        print(f"Warning: Image not found: {full_path}")
        return ""
    
    try:
        with open(full_path, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
        
        # Determine MIME type from extension
        ext = Path(image_path).suffix.lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.ico': 'image/x-icon',
            '.svg': 'image/svg+xml'
        }
        mime_type = mime_types.get(ext, 'image/png')
        
        return f"data:{mime_type};base64,{img_data}"
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return ""

def embed_images_in_html(html_content, image_folder='icons'):
    """
    Replace file:// image src attributes with base64 data URIs
    
    Args:
        html_content: HTML string with file:// image references
        image_folder: Folder containing images (relative to app root)
    
    Returns:
        Modified HTML with embedded base64 images
    """
    import re
    
    # Pattern to match file:// image sources
    # Handles: <img src="file:///path/to/image.png">
    pattern = r'<img\s+src="file:///[^"]*?([^/]+\.(png|jpg|jpeg|gif|ico|svg))"'
    
    def replace_with_base64(match):
        filename = match.group(1)
        image_path = os.path.join(image_folder, filename)
        base64_uri = get_image_as_base64(image_path)
        
        if base64_uri:
            # Replace the entire src attribute
            return f'<img src="{base64_uri}"'
        else:
            # Keep original if conversion failed
            return match.group(0)
    
    modified_html = re.sub(pattern, replace_with_base64, html_content)
    return modified_html

class ReadmeViewer(QMainWindow):
    """
    Reusable README viewer window with HTML support and embedded images
    
    Usage:
        viewer = ReadmeViewer(
            html_file='README.html',
            title='User Guide',
            window_icon='icons/favicon.ico',
            image_folder='icons'
        )
        viewer.show()
    """
    
    def __init__(self, html_file='README.html', title='Documentation', 
                 window_icon=None, image_folder='icons', parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(title)
        self.resize(900, 700)
        
        # Set window icon if provided
        if window_icon:
            icon_path = get_resource_path(window_icon)
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create text browser for HTML display
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)  # Allow clicking links
        layout.addWidget(self.text_browser)
        
        # Load and display HTML
        self.load_html(html_file, image_folder)
    
    def load_html(self, html_file, image_folder):
        """Load HTML file and embed images"""
        html_path = get_resource_path(html_file)
        
        if not os.path.exists(html_path):
            error_html = f"""
            <html>
            <body style="font-family: Arial; padding: 20px;">
                <h1 style="color: red;">Error</h1>
                <p>README file not found: <code>{html_path}</code></p>
            </body>
            </html>
            """
            self.text_browser.setHtml(error_html)
            return
        
        try:
            # Read HTML content
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Embed images as base64
            html_with_images = embed_images_in_html(html_content, image_folder)
            
            # Display in text browser
            self.text_browser.setHtml(html_with_images)
            
        except Exception as e:
            error_html = f"""
            <html>
            <body style="font-family: Arial; padding: 20px;">
                <h1 style="color: red;">Error Loading README</h1>
                <p>{str(e)}</p>
            </body>
            </html>
            """
            self.text_browser.setHtml(error_html)
            print(f"Error loading README: {e}")

# Standalone test function
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    viewer = ReadmeViewer(
        html_file='README.html',
        title='Task Buddy - User Guide',
        window_icon='icons/favicon.ico',
        image_folder='icons'
    )
    viewer.show()
    sys.exit(app.exec())