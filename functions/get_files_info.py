import os 
def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
        working_directory: the base start search from 
        directory: the directory we LLM want 
    """
    try:
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'

        working_dir_abs : str = os.path.abspath(working_directory)
        target_dir : str = os.path.normpath( os.path.join(working_dir_abs, directory))
        valid_target_dir : bool = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f'Error: {e}'
