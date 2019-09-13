# Step Definition Scanner

The Step Definition Scanner scans files for Cucumber C++ Step Definitons and stores informations about each found Step Definition in a json and a csv file.

## Build:
This description is for creating executable on Windows with pyinstaller.\
pyinstaller can be found here: [pyinstaller.org](https://www.pyinstaller.org/).

in terminal enter:
```
pyinstaller --noconsole -i icon.ico StepDefinitionScanner.py -y
copy icon.ico dist\StepDefinitionScanner
```

build will be in folder dist\StepDefinitionScanner\
\
Inside the dist folder you will find a zip file containing a preebuild version ready to run. Just unzip the archieve and run the StepDefinitionScanner.exe

## Run:
To run the Step Definition Scanner just start the executable.\
Enter a Path where to start searching. Search is recursive and scans all sub dirs so be aware to choose a meaningful starting dir.\
Enter a file postfix. postfix can just be .cpp, the hole file name or just the last part of filename.\
Hit 'Run Scanner' and wait for 'Done' to show up.\
Result will be stored in StepDefinition.json and StepDefinition.csv in the dir where the executable is placed.

## Informations:
### Annotations and macros
The Step Definition Scanner Scans for default Cucumber C++ macros ```CUKE_STEP_```, ```GIVEN```, ```WHEN```, ```THEN``` and ```REGEX_PARAM```.\
But it also scanns for ```//@OBJECT_TYPE: ```. This is a self defined annotation for adding information about the Object wich the Step Definition is made for. 
For example: If you write a StepDefinition for pushing a QPushButton the annation could look this: ```//@OBJECT_TYPE: QPushButton```. 
Place the annotation just above the Step Definition:\
```
//@OBJECT_TYPE: QPushButton
CUKE_STEP_("^i click the button (.+)$") {
	REGEX_PARAM(std::string, buttonName);

	QPushButton* pushButton = getObjectbyName<QPushButton>(buttonName);
	QVERIFY2(pushButton != nullptr, "The button could not be found.");
	pushButton->click();
}
```
### WebView
This reposetory contains a webview.html for displaying the results in a nice table. The webview page musst be opend on a webserver because it loads the StepDefnition.json using http-request.\
One simple soloution to this is using Web Server for Chrome.