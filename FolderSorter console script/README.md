### Folder sorter

Many people have a folder on their desktop called something like "Disassemble". As a rule, hands never manage to 
disassemble this folder.

In this task we will make a folder parsing script into a Python package and a console script that can be called 
anywhere on the system from the console with the clean-folder command. To do this, we need to create a file and 
folder structure:

    ├── clean_folder
    │    ├── clean_folder
    │    │   ├── clean.py
    │    │   └── __init__.py
    │    └── setup.py


This program can sort such extension:

    Images ('JPEG', 'PNG', 'JPG', 'SVG')
    Video files ('AVI', 'MP4', 'MOV', 'MKV')
    Documents ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    Music ('MP3', 'OGG', 'WAV', 'AMR')
    Archives ('ZIP', 'GZ', 'TAR')
    Unknown extensions

The output of the script includes:

    A list of files in each category (music, video, photos, etc.)
    A list of all recognized script extensions found in the target folder.
    A list of all extensions that are unknown to the script.

Example of running a script:

     The package is installed on the system with the *pip install -e* command. (or *python setup.py install*, requires 
     admin rights).
     After installation, the *clean_folder* package appears in the system.
     When the package is installed on the system, the script can be called anywhere from the console with the 
     *clean-folder* command.
     A console script handles command line arguments exactly like a Python script.