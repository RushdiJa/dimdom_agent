import os

def is_safe_path(outter_directory: str, inner_directory: str) -> bool:
    outter_directory_abs : str = os.path.abspath(outter_directory)
    target_directory : str = os.path.normpath(os.path.join(outter_directory_abs, inner_directory))
    valid_target_directory : bool = os.path.commonpath([outter_directory_abs, target_directory]) == outter_directory_abs
    return valid_target_directory
