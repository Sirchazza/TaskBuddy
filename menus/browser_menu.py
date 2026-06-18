from PySide6.QtGui import QIcon, QAction
import webbrowser as web
import urllib.parse
from utils import ClipboardUtils as Clip
from utils import PopupManager


class BrowserMenu:
    """Handles the Browser menu creation and related functions"""
    
    def __init__(self, parent_app):
        """
        Args:
            parent_app: Reference to main app for accessing helper methods
        """
        self.app = parent_app
    
    def create_menu(self, parent_menu):
        
        Browser_menu = parent_menu.addMenu("🌐 Browser Functions") # Web based utilities
        
        web_search = QAction(self.app.icon_cache.get('google', QIcon()), "Google Search", parent_menu)
        web_search.triggered.connect(self.google_search)
        Browser_menu.addAction(web_search)
        
        url_pointer = QAction(self.app.icon_cache.get('chrome', QIcon()),"Go To Website", parent_menu)
        url_pointer.triggered.connect(self.google_search)
        Browser_menu.addAction(url_pointer)
        
        snow_search = QAction(self.app.icon_cache.get('snow', QIcon()), "Search Service Now Ticket", parent_menu)
        snow_search.triggered.connect(self.service_now)
        Browser_menu.addAction(snow_search)
        

# -------- Brower based operations -------- #

    def service_now(self): # Navigates to the highlighted ticket number in ServiceNow using Google Chrome
        selected = Clip.get_selected_text()
        if not selected:
            PopupManager.warning("Silly Billy!", "You need to highlight some text 1st!")
            return
        
        browser = web.Chrome("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        
        text=selected.strip()
        
        sn_url = fr"https://jll.service-now.com/now/nav/ui/search/0f8b85d0c7922010099a308dc7c2606a/params/search-term/{urllib.parse.quote(text)}/global-search-data-config-id/c861cea2c7022010099a308dc7c26041/search-context/now%2Fnav%2Fui"
        browser.open_new_tab(sn_url)

    def google_search(self): # Using Google Chrome, either performs a google search or navigates to a webpage depending on if the seleceted text is a URL
        selected = Clip.get_selected_text()
        if not selected:
            PopupManager.warning('Silly Billy!', 'No text selected. What am I searching for?')
            return
        
        browser = web.Chrome("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        
        text = selected.strip()
        
        if text.startswith(('https', 'http', 'www')):
            if text.startswith('www.'):
                text = 'https://' + text
            browser.open_new_tab(text)
        else:
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(text)}"
            browser.open_new_tab(search_url)