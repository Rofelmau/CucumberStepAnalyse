# Step Definition Scanner

The Step Definition Scanner scans your files for Cucumber C++ Step Definitons and stores data about each found Step Definition in a json and a csv file.

## Build:
This description is for creating executable on Windows with pyinstaller.\
pyinstaller can be found here: [pyinstaller.org](https://www.pyinstaller.org/).

in terminal enter:
```
pyinstaller --noconsole -i icon.ico StepDefinitionScanner.py -y
copy icon.ico dist\StepDefinitionScanner
```

build will be in folder dist\StepDefinitionScanner

## Run:
To run the Step Definition Scanner just start the executable.\
Enter a Path where to start searching. Search is recursive and scans all sub dirs so be aware to choose a god starting dir.\
Enter a file postfix. postfix can just be .cpp, the hole file name or just the last part of filename.\
Hit 'Run Scanner' and wait for 'Done' to show up.\
Result will be stored in StepDefinition.json in the dir where the executable is placed.