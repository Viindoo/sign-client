Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' Get the directory containing the VBS script
strScriptPath = WScript.ScriptFullName
strAppPath = FSO.GetParentFolderName(strScriptPath)

' Set working directory
WshShell.CurrentDirectory = strAppPath

' Build the full path to Python executable and main.py
strPythonPath = FSO.BuildPath(strAppPath, ".venv\Scripts\python.exe")
strMainPath = FSO.BuildPath(strAppPath, "main.py")

' Run the application
WshShell.Run """" & strPythonPath & """ """ & strMainPath & """", 0, False
