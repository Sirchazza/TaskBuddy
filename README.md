<h1>Task Buddy - User Guide</h1>

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [📅 Insert Date/Time](#-insert-datetime)
	- [ISO Format](#iso-format)
	- [UK Format](#uk-format)
	- [USA Format](#usa-format)
	- [How to Use Insert Date/Time Functions](#how-to-use-insert-datetime-functions)
- [🔤 Change Case](#-change-case)
	- [Uppercase](#uppercase)
	- [Lowercase](#lowercase)
	- [Title Case](#title-case)
	- [Sentence Case](#sentence-case)
	- [How to Use Change Case Functions](#how-to-use-change-case-functions)
- [🔄 Text Replacements](#-text-replacements)
	- [Quick Replacements](#quick-replacements)
		- [How to Use Quick Replacements:](#how-to-use-quick-replacements)
	- [Custom Replacements](#custom-replacements)
		- [How to Use Custom Replacements:](#how-to-use-custom-replacements)
- [📝 Line Operations](#-line-operations)
	- [Remove Line Breaks](#remove-line-breaks)
	- [Add Line Numbers](#add-line-numbers)
	- [Sort Lines A-Z](#sort-lines-a-z)
	- [How to Use Line Operation Functions](#how-to-use-line-operation-functions)
- [🛢 SQL Functions](#-sql-functions)
	- [Wrap Text With L/R Trim](#wrap-text-with-lr-trim)
	- [Wrap Text With Trim](#wrap-text-with-trim)
	- [Move Commas To Front (All)](#move-commas-to-front-all)
	- [Move Commas To Front (exc. 1st)](#move-commas-to-front-exc-1st)
	- [Excel Columns to SQL](#excel-columns-to-sql)
	- [Remove Square Brackets](#remove-square-brackets)
	- [How to Use SQL Functions](#how-to-use-sql-functions)
- [🌐 Browser Functions](#-browser-functions)
	- [Google Search](#google-search)
	- [Go To Website](#go-to-website)
	- [Search Service Now Ticket](#search-service-now-ticket)
	- [How to Use Browser Functions](#how-to-use-browser-functions)
- [📝 Snippets](#-snippets)
	- [Overview](#overview)
	- [Using Snippets](#using-snippets)
	- [Creating Custom Snippets](#creating-custom-snippets)
		- [Simple Snippet Formatting](#simple-snippet-formatting)
		- [Snippet with Parameters Formatting](#snippet-with-parameters-formatting)
		- [Parameter Naming](#parameter-naming)
	- [Tips for Effective Snippets](#tips-for-effective-snippets)
	- [Reloading Snippets](#reloading-snippets)
- [Troubleshooting](#troubleshooting)
	- ["Silly Billy!" Warning Messages](#silly-billy-warning-messages)
	- [Menu Doesn't Appear:](#menu-doesnt-appear)
	- [File Operations Don't Work](#file-operations-dont-work)
	- [Browser Functions Open Wrong Browser](#browser-functions-open-wrong-browser)
	- [Getting Help](#getting-help)
- [Tips and Best Practices](#tips-and-best-practices)


## Introduction

Text Tools is a Windows utility application that provides quick access to text manipulation, file operations, and productivity functions through a convenient hotkey-activated menu. The application runs in the system tray and can be accessed at any time with a simple keyboard shortcut.


## Getting Started

1. Launch the Application: Run Task Buddy.exe
2. Locate the Tray Icon: Look for the Text Tools icon in your system tray (bottom-right corner of Windows taskbar)
3. Access the Menu: Press Alt+Shift+. (using the decimal point on the numpad) to open the menu at your cursor position
4. Pause/Resume: Right-click the tray icon to pause or resume the hotkey listener if needed

## 📅 Insert Date/Time

Insert the current date and/or time in various standardized formats.


### ISO Format

ISO Format uses the international standard with year first: 2026-06-02 14:30 (YYYY-MM-DD HH:MM)

Example:

| **Current Date & Time** | **Date Only** | **Time Only** |
|:-----------------------:|:-------------:|:-------------:|
|     2026-06-02 14:30    |   2026-06-02  |     14:30     |


### UK Format

UK Format uses a date format with the day first: 02-06-2026 14:30  (DD-MM-YYYY HH:MM)

Example:

| **Current Date & Time** | **Date Only** | **Time Only** |
|:-----------------------:|:-------------:|:-------------:|
|     02-06-2026 14:30    |   02-06-2026  |     14:30     |


### USA Format

USA Format uses a date format with the month first: 06-02-2026 14:30  (MM-DD-YYYY HH:MM)

Example:

| **Current Date & Time** | **Date Only** | **Time Only** |
|:-----------------------:|:-------------:|:-------------:|
|     06-02-2026 14:30    |   06-02-2026  |     14:30     |


### How to Use Insert Date/Time Functions

1. Position your cursor where you want the date/time inserted
2. Open the Text Tools menu (Alt+Shift+.)
3. Navigate to 📅 Insert Date/Time
4. Select your preferred format and option
5. The date/time will be automatically inserted at your cursor position


## 🔤 Change Case

Convert selected text between different case formats.


### Uppercase

Converts all characters to uppercase

Example:

	Original Text:  
		hello world

	Result:  
		HELLO WORLD


### Lowercase

Converts all characters to lowercase

Example:

	Original Text:  
		HELLO WORLD

	Result:  
		hello world


### Title Case

Capitalizes The First Letter Of Each Word

Example:

	Original Text:  
		HELLO WORLD

	Result:  
		Hello World


### Sentence Case

Capitalizes only the first letter

Example:

	Original Text:  
		HELLO WORLD

	Result:  
		Hello world

### How to Use Change Case Functions

1. Highlight/select the text you want to convert
2. Open Text Tools menu (Alt+Shift+.)
3. Navigate to 🔤 Change Case
4. Select your desired case format
5. The selected text will be replaced with the converted version


## 🔄 Text Replacements

Replace specific characters or patterns in selected text using either:  
- One of multiple pre-defined replacement options  
- Entering the text being replaced and what it is being replaced by


### Quick Replacements

Replaces characters in the highlighted text using pre-defined rules:

- Spaces to Underscores: Hello World → Hello_World
- Spaces to Hyphens: Hello World → Hello-World

- Hyphens to Spaces: Hello-World → Hello World
- Hyphens to Underscores: Hello-World → Hello_World

- Underscores to Hyphens: Hello_World → Hello-World
- Underscores to Spaces: Hello_World → Hello World


#### How to Use Quick Replacements:

1. Highlight the text containing the substring you want to replace
2. Open Text Tools menu
3. Select your desired replacement option
4. The text will be updated automatically


### Custom Replacements

The Custom String replacement option allows you to replace any text with text.


#### How to Use Custom Replacements:

1. Highlight the text containing the substring you want to replace  
2. Open Text Tools menu  
3. Select 🔄 Text Replacements → Custom String  
4. Enter the text to replace in the first dialog box  
5. Enter the replacement text in the second dialog box  
6. The text will be updated automatically  

Example:

	Original text:
		"We will say hello when we get there"
    Replace text:
		"We"
    Replace with:
		"I"
	Result:
		"I will say hello when I get there"


## 📝 Line Operations

Manipulate text on a line-by-line basis.


### Remove Line Breaks

Combines all highlighted lines into a single line, removing any spaces at the beginning and end of the combined sentence

Example:

	Original Text:  
		First Line,  
		Second Line

	Result:  
		First Line, Second Line


### Add Line Numbers

Adds numbering and removes leading and trailing spaces to each line in the highlighted text  

Example:

	Original Text:  
		First line,  
		Second line

	Result:  
    	1. First line,  
    	2. Second line


### Sort Lines A-Z

Alphabetically sorts all lines in the highlighted text.  
Works with both text and numbers.

Example:

	Original Text:  
		A banana
		5 apples  
		2 pears
		3 peaches
		4 melons

	Result:  
		2 pears
		3 peaches
		4 melons
		5 apples  
		A banana

### How to Use Line Operation Functions

1. Select the multi-line text you want to manipulate
2. Open Text Tools menu
3. Navigate to 📝 Line Operations
4. Choose your desired operation
5. The modified text replaces the original selection


## 🛢 SQL Functions

Utilities for working with SQL code and queries.


### Wrap Text With L/R Trim

Wraps the highlighted text with LTRIM(RTRIM(...))  
Used for Legacy SQL Server databases to strip whitespace from the beginning and end of text

Example:

	Text:
		sName

	Result:
		LTRIM(RTRIM(sName))


### Wrap Text With Trim

Wraps selected text with TRIM(...)  
Used for modern SQL Server databases to strip whitespace from the beginning and end of text (SQL Server 2017+)

Example:

	Text:
		sName

	Result:
		TRIM(sName)


### Move Commas To Front (All)

Moves trailing commas to the beginning of each line  
Applies to all lines including the first

Example:

	Selected Text:
		sName,
		sDesc,
		sDate,
		iType

	Result:
		,sName
		,sDesc
		,sDate
		,iType


### Move Commas To Front (exc. 1st)

Moves trailing commas to the beginning of each line  
Excludes the first line (useful for SELECT statements)

Example:

	Selected Text:
		sName,
		sDesc,
		sDate,
		iType

	Result:
		sName
		,sDesc
		,sDate
		,iType


### Excel Columns to SQL

Converts tab-separated Excel columns to SQL-formatted column list  
Adds proper indentation and commas

Example:

	Selected Text (Copied from Excel):
		Property_Code	Tenant_Code	Unit_Code	Status	First_Name	Last_Name
		

	Result:
		Property_Code
		, Tenant_Code
		, Unit_Code
		, Status
		, First_Name
		, Last_Name


### Remove Square Brackets

Strips [ and ] characters from the selected text  
Useful for cleaning copied SQL Server object names

Example:

	Selected Text:
		[sName],
		[sDesc],
		[sDate],
		[iType]

	Result:
		sName,
		sDesc,
		sDate,
		iType


### How to Use SQL Functions

1. Select the SQL code or text you want to modify
2. Open Text Tools menu
3. Navigate to 🛢 SQL Functions
4. Select your desired operation
5. The modified code replaces the original selection


## 🌐 Browser Functions

Open web-based resources directly from selected text


### Google Search

Performs a Google search for selected text in a new Chrome tab


### Go To Website

Opens URLs in a new Chrome tab


### Search Service Now Ticket

Searches JLL's ServiceNow instance for highlighted ticket numbers


### How to Use Browser Functions

1. Highlight the text, URL, or ticket number
2. Open Text Tools menu
3. Navigate to 🌐 Browser Functions
4. Select your desired action
5. A new Chrome tab will open with the results

Requirement: Google Chrome must be installed at the default location


## 📝 Snippets

Insert customizable text snippets with optional parameters.

### Overview

Snippets allow you to create reusable text templates that can be quickly inserted.  
They support both static text and dynamic parameters that prompt for input when used.

### Using Snippets

1. Open Text Tools menu
2. Navigate to 📝 Snippets
3. Browse through categories (e.g., SQL, Excel, Python)
4. Select your desired snippet
5. If the snippet has parameters, popup boxes will prompt for input
6. The completed snippet will be inserted at your cursor position


### Creating Custom Snippets

Snippets are stored in the snippets.toml file located in the same directory as the application.  
If a snippets.toml file is not found, one will be created with with some sample snippets.  
The app will need to be closed and reopened for the new snippets to be added to the menu.

#### Simple Snippet Formatting

For a snippet with no blanks that need to be filled, the below format is used:

	["Category/Snippet Name"]
	text = "Your snippet content here"

	Example:
		["Email/Signature"]
		text = """Best regards,
		John Smith
		Senior Analyst
		john.smith@company.com"""

Below is a preview of how this would appear in the menu:

![alt text](image.png)


#### Snippet with Parameters Formatting

You can also add a snippet that has blanks, allowing you to fill them in when generating it.  
Below is the format for a sinppet with blanks (parameters):

	["Category/Snippet Name"]
	text = """Your snippet with {parameter1} and {parameter2}"""
	params = ["parameter1", "parameter2"]

	Example:  
		["SQL/Custom Query"]
		text = """SELECT
			{columns}
		FROM
			{table_name}
		WHERE
			{condition}
		ORDER BY
			{order_column};"""
		params = ["columns", "table_name", "condition", "order_column"]

When used, this snippet will prompt you four times:  

1. "Enter Columns:"  
2. "Enter Table Name:"  
3. "Enter Condition:"  
4. "Enter Order Column:"  

Below is an example of a prompt that will open:

![alt text](image-1.png)


#### Parameter Naming

Use snake_case for parameter names (e.g., table_name, order_by)  
The app automatically converts snake_case to "Title Case" in the prompts
from_table becomes "Enter From Table:"
order_by becomes "Enter Order By:"


### Tips for Effective Snippets

1. Use descriptive names: Make snippet names clear and searchable
2. Add comments: Use TOML comments (#) to document complex snippets
3. Test parameters: Ensure parameter names make sense when converted to prompts
4. Special characters: Escape special characters if needed (e.g., \\ for backslash)

### Reloading Snippets

After editing snippets.toml:

- Close and restart the Text Tools application. Your new snippets will appear in the menu
- If the snippets.toml file is missing or corrupted, the application will automatically create a sample file with example snippets.


## Troubleshooting

### "Silly Billy!" Warning Messages

These appear when you haven't selected/highlighted text before using a text manipulation function
Solution: Highlight the text you want to modify before opening the menu


### Menu Doesn't Appear:

1. Ensure the hotkey Alt+Shift+. (numpad decimal) is being pressed correctly
2. Check if the hotkey is paused (right-click tray icon to check status)
3. Verify the application is running (look for tray icon)


### File Operations Don't Work

1. Ensure you've selected the correct file type in File Explorer
2. For MS Project conversion: Verify Java Runtime Environment is installed
3. For image conversion: Check the source file isn't corrupted


### Browser Functions Open Wrong Browser

1. Browser functions are hardcoded to use Google Chrome
2. Ensure Chrome is installed at: C:\Program Files\Google\Chrome\Application\chrome.exe


### Getting Help

If you encounter issues not covered here:

1. Check that all file paths are accessible
2. Verify required software (Word, Chrome, Java) is installed
3. Restart the application
4. Check for any error messages in the console (if running from source)


## Tips and Best Practices

1. Learn the Categories: Familiarize yourself with the menu structure to quickly find functions
2. Create Snippets: Build a personal library of frequently used text patterns
3. Use Hotkey Efficiently: Keep one hand near the numpad for quick access
4. Test Operations: Try text operations on sample data before using on important content
5. Organize Snippets: Use clear category names in your snippets.toml file