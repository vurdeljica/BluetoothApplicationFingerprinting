# BluetoothApplicationFingerprinting

## Project description
Idea behind this project is to fingerprint application using bluetooth communication.

## Project setup
In order to use project adb is required.  
Adb can be obtained from: [SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)  
After download, add path to adb in Environment Variable Path.

Used modules in this project:  
\- btsnoop

Remarks: btsnoop.py has a bug in it. Add `import pckgutil` at the beginning of file.