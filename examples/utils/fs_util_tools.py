from langchain_core.tools import tool
import os

@tool
def read_file_tool(file_path: str):
    """
    Read a file and return the contents.
    
    Handles both absolute and relative file paths. Relative paths are resolved 
    from the current working directory.
    
    Args:
        file_path (str): Path to the file to read (absolute or relative)
        
    Returns:
        str: The contents of the file
    """
    try:
        # Convert relative path to absolute path
        abs_path = os.path.abspath(file_path)
        print(f"Reading file: {abs_path}")
        
        if not os.path.exists(abs_path):
            return f"Error: File '{file_path}' not found at '{abs_path}'"
            
        if not os.path.isfile(abs_path):
            return f"Error: '{file_path}' is not a file"
            
        with open(abs_path, "r", encoding="utf-8") as file:
            content = file.read()
            return content
            
    except PermissionError:
        return f"Error: Permission denied reading file '{file_path}'"
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"

@tool
def list_path_contents_tool(directory_path: str):
    """
    List all files and directories in the specified path.
    
    Handles both absolute and relative directory paths. Relative paths are 
    resolved from the current working directory.
    
    Args:
        directory_path (str): Path to the directory to list (absolute or relative)
        
    Returns:
        list: List of files and directories in the path
    """
    try:
        # Convert relative path to absolute path
        abs_path = os.path.abspath(directory_path)
        print(f"Listing contents of: {abs_path}")
        
        if not os.path.exists(abs_path):
            return f"Error: Directory '{directory_path}' not found at '{abs_path}'"
            
        if not os.path.isdir(abs_path):
            return f"Error: '{directory_path}' is not a directory"
        
        # Get all files and directories
        contents = []
        for item in os.listdir(abs_path):
            item_path = os.path.join(abs_path, item)
            if os.path.isfile(item_path):
                contents.append(f"[FILE] {item}")
            elif os.path.isdir(item_path):
                contents.append(f"[DIR] {item}")
            else:
                contents.append(f"[OTHER] {item}")
                
        return contents
        
    except PermissionError:
        return f"Error: Permission denied accessing directory '{directory_path}'"
    except Exception as e:
        return f"Error listing directory '{directory_path}': {str(e)}"