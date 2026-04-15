import sys
import shutil

def delete_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Directory {path} deleted successfully.")
    else:
        print(f"Directory {path} does not exist.")

delete_directory("test")



"""this repository is a clone of the original repository, but with the commits deleted."""