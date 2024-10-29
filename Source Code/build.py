# Import libraries
import os
from os import mkdir
import shutil
from setuptools.compat.py311 import shutil_rmtree
import time

# Find the downloads folder
downloads_folder = os.path.expanduser('~/Downloads') # Find where the downloads folder is located
print("The package will now be installed into the downloads folder")

# Make a new folder in the downloads folder for the package to be created
mkdir(downloads_folder + "/Package")

# Copy the main contents to the package directory
shutil.copy("main.py", downloads_folder + "/Package/main.py")
shutil.copy("settings.ini", downloads_folder + "/Package/settings.ini")
shutil.copy("Database.accdb", downloads_folder + "/Package/Database.accdb")

# Run pyinstaller to convert the python file into an executable .exe file
os.chdir(downloads_folder + "/Package")
os.system("pyinstaller -F main.py --collect-all customtkinter -w")

# Move all the files into a single directory
shutil.copy(downloads_folder + "/Package/dist/main.exe", downloads_folder + "/Package")
os.remove ("main.spec")
os.remove("main.py")
shutil_rmtree(downloads_folder + "/Package/dist")
shutil_rmtree(downloads_folder + "/Package/build")

# Compress it all into a .zip file
shutil.make_archive(downloads_folder + "/flight-logbook", "zip", downloads_folder + "/Package")