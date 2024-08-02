import os
import shutil
def copy_content(source, destination):
    if(os.path.exists(destination)):
        shutil.rmtree(destination)
    os.mkdir(destination)
    make_copies(source, destination)

def make_copies(source, destination):
    for item in os.listdir(source):
        new_path = os.path.join(source, item)
        if os.path.isfile(new_path):
            print(shutil.copy(new_path, destination))
        else:
            new_dest = os.path.join(destination, item)
            if(not os.path.exists(new_dest)):
                os.mkdir(new_dest)
            copy_content(new_path, new_dest)
