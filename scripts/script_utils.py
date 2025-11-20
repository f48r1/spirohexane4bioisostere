def append_parent(current_path):
    import os
    import sys

    caller_file = os.path.abspath(current_path)
    parent_dir = os.path.dirname(caller_file)
    if parent_dir not in sys.path:
        sys.path.append(parent_dir) # NOTE allowing import of src module

def change2parent(current_path):
    import os

    caller_file = os.path.abspath(current_path)
    parent_dir = os.path.dirname(caller_file)
    os.chdir(parent_dir)
    print(f"[INFO] Working directory changed to: {parent_dir}")