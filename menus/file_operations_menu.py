import os
import sys
import re
import jpype
import win32com.client
import pyperclip
import pandas as pd
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageFile
from zipfile import ZipFile
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QAction, QIcon
from utils import FileExplorerUtils as exp
from utils import ProgressBar, PopupManager

class FileOperationsMenuHandler:
    """Handles file operations menu creation and related functions"""
    
    def __init__(self, parent_app):
        """
        Args:
            parent_app: Reference to main app for accessing helper methods
        """
        self.app = parent_app
    
    def create_menu(self, parent_menu):
        """Create and return the File Specific Functions submenu"""
        file_menu = parent_menu.addMenu("📄 File Specific Functions")
        
        # MS Word submenu
        self._create_word_menu(file_menu)
        
        # Images submenu
        self._create_image_menu(file_menu)
        
        # MS Project submenu
        self._create_project_menu(file_menu)
        
        # Zip Files submenu
        self._create_zip_menu(file_menu)
        
        return file_menu
    
    def _create_word_menu(self, parent_menu):
        """Create MS Word submenu"""
        msword_menu = parent_menu.addMenu(
            self.app.icon_cache.get('word', QIcon()),
            "MS Word"
        )
        
        word_field_codes = QAction(
            self.app.icon_cache.get('word', QIcon()),
            "Copy Word Field Codes",
            parent_menu
        )
        word_field_codes.triggered.connect(self.copy_field_codes)
        msword_menu.addAction(word_field_codes)
    
    def _create_image_menu(self, parent_menu):
        """Create Images submenu"""
        image_menu = parent_menu.addMenu(
            self.app.icon_cache.get('picture', QIcon()),
            "Images"
        )
        
        img_convert = QAction(
            self.app.icon_cache.get('icon', QIcon()),
            "Convert to .ico",
            parent_menu
        )
        img_convert.triggered.connect(self.convert_image)
        image_menu.addAction(img_convert)
    
    def _create_project_menu(self, parent_menu):
        """Create MS Project submenu"""
        project_menu = parent_menu.addMenu(
            self.app.icon_cache.get('project', QIcon()),
            "MS Project"
        )
        
        mpp_to_excel = QAction(
            self.app.icon_cache.get('project', QIcon()),
            "Convert to Excel",
            parent_menu
        )
        mpp_to_excel.triggered.connect(lambda: self.convert_project_file('xlsx'))
        project_menu.addAction(mpp_to_excel)
        
        # TODO:
        # mpp_to_pdf = QAction(
        #     self.app.icon_cache.get('project', QIcon()),
        #     "Convert to PDF",
        #     parent_menu
        # )
        # mpp_to_pdf.triggered.connect(lambda: self.convert_project_file('pdf'))
        # project_menu.addAction(mpp_to_pdf)
    
    def _create_zip_menu(self, parent_menu):
        """Create Zip Files submenu"""
        zip_menu = parent_menu.addMenu(
            self.app.icon_cache.get('zip_folder', QIcon()),
            "Zip Files"
        )
        
        unzip_multiple = QAction(
            self.app.icon_cache.get('zip_folder', QIcon()),
            "Unzip Folders",
            parent_menu
        )
        unzip_multiple.triggered.connect(self.unzip_multiple_folders)
        zip_menu.addAction(unzip_multiple)
    
    # -------- File based operations -------- #
    
    def copy_field_codes(self):
        """Runs a macro to extract full Mail Merge Field Codes"""
        word = win32com.client.GetActiveObject("Word.Application")
        word.Run("CopyFieldCodesAsText")
        
        PopupManager.info(r"Gotcha!", fr"Copied: {pyperclip.paste()}")
    
    def convert_image(self):
        """Converts images to .ico format"""
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        selected = exp.get_explorer_selection()
        if selected is None:
            PopupManager.warning('Silly Billy!', "You didn't pick a file!")
            return
        else:
            filepath = Path(selected)
        
        img = Image.open(filepath).convert('RGBA')
        
        icon_size = [(32, 32)]
        img.save(filepath.with_suffix('.ico'), format='ICO', sizes=icon_size)
        PopupManager.info(r"File Converted!", fr"File Converted: {filepath.with_suffix('.ico')}")
    
    def convert_project_file(self, filetype):
        """Convert MS Project file to Excel or PDF"""
        
        self.progressbar = ProgressBar(
            title="Convert Project File to Excel",
            message="Getting filepath...",
            maximum=100
        )
        self.progressbar.show()
        
        selected_file = exp.get_explorer_selection()
        if selected_file is None:
            self.progressbar.close()
            PopupManager.warning('Silly Billy!', 'The path used is not a valid path')
            return
        else:
            filepath = Path(selected_file)
        
        # Initialize JPype with proper path handling for PyInstaller
        if not jpype.isJVMStarted():
            try:
                # Determine if running as script or bundled executable
                if getattr(sys, 'frozen', False):
                    # Running as PyInstaller bundle
                    bundle_dir = sys._MEIPASS
                    mpxj_dir = os.path.join(bundle_dir, 'mpxj')
                else:
                    # Running as script
                    import mpxj as mpxj_module
                    mpxj_dir = os.path.dirname(mpxj_module.__file__)
                
                # Find all JAR files in mpxj directory
                jar_files = []
                for root, dirs, files in os.walk(mpxj_dir):
                    for file in files:
                        if file.endswith('.jar'):
                            jar_files.append(os.path.join(root, file))
                
                if jar_files:
                    jpype.startJVM(classpath=jar_files)
                else:
                    jpype.startJVM()  # Let jpype find JVM itself
                
            except Exception as e:
                self.progressbar.close()
                PopupManager.warning('Java Error', f'Failed to start Java VM: {str(e)}')
                return
        
        try:
            from org.mpxj.mpp import MPPReader  # pyright: ignore[reportMissingImports]
        except Exception as e:
            self.progressbar.close()
            PopupManager.warning('Import Error', f'Failed to import MPPReader: {str(e)}')
            return
        
        project = MPPReader().read(filepath)
        
        self.progressbar.max(sum(1 for task in project.getTasks() if task.getName()) + 2)
        
        tasks_data = []
        pattern = re.compile(r'-?\d*\.?\d+')
        flag = 0
        
        for task in project.getTasks():
            if not task.getName():
                if flag == 0:
                    tasks_data.append({
                        'TaskNumber': '',
                        'Name': '',
                        'Start': '',
                        'Finish': '',
                        'Duration': ''
                    })
                    flag = 1
                continue
            
            match = pattern.search(str(task.getDuration()))
            duration = float(match.group()) if match else 0
            outline_number = task.getOutlineNumber()
            indent = '    ' * (int(task.getOutlineLevel()) - 1)
            name = re.sub(r'^\d{2} - ', '', str(task.getName()))
            
            self.progressbar.increment(f"Importing Task: {str(task.getName())}")
            tasks_data.append({
                'TaskNumber': outline_number,
                'Name': f"{indent}{name}",
                'Start': datetime.fromisoformat(str(task.getStart())).strftime("%d/%m/%Y"),
                'Finish': datetime.fromisoformat(str(task.getFinish())).strftime("%d/%m/%Y"),
                'Duration': int(duration) if duration.is_integer() else duration
            })
            flag = 0
        
        df = pd.DataFrame(tasks_data)
        
        if filetype == 'xlsx':
            self.progressbar.increment("Converting to Excel File")
            df.to_excel(filepath.with_suffix('.xlsx'), index=False)
            self.progressbar.close()
            PopupManager.info(
                r"File Converted!",
                fr"MS project file Converted: {filepath.with_suffix('.xlsx')}"
            )
        
        # TODO: Uncomment and test PDF conversion when ready
        # elif filetype == 'pdf':
        #     self._convert_to_pdf(filepath, df)
    
    # def _convert_to_pdf(self, filepath, df):
    #     """Convert project data to PDF with Gantt chart"""
    #     import matplotlib.pyplot as plt
    #     import matplotlib.dates as mdates
    #     from matplotlib.backends.backend_pdf import PdfPages
    #     
    #     # PDF conversion logic here...
    #     pass
    
    def unzip_multiple_folders(self):
        """Unzip multiple zip files to a selected folder"""
        selected = exp.get_explorer_selection("multiple")
        if selected is None:
            PopupManager.warning('Silly Billy!', "You didn't select a file!")
            return
        
        output_folder = exp.get_folder_path(selected[0])
        if not output_folder:
            PopupManager.warning('Silly Billy!', "You didn't select an output folder!")
            return
        
        for archive in selected:
            filepath = Path(archive)
            if filepath.suffix != ".zip":
                continue
            
            with ZipFile(filepath) as zipped:
                zipped_files = zipped.namelist()
                for filename in zipped_files:
                    output_file = output_folder / filename
                    if output_file.is_file():
                        button = PopupManager.question(
                            "Existing File Found",
                            f"{filename} already exists in this folder. Would you like to overwrite the existing file?",
                        )
                        if button == QMessageBox.No:
                            continue
                    zipped.extract(filename, output_folder)