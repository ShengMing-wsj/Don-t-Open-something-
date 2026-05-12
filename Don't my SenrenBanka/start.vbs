Dim objShell
Set objShell = CreateObject("WScript.Shell")

Dim scriptDir
scriptDir = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))

objShell.Run "pythonw.exe """ & scriptDir & "Don't Open my Privacy.py""", 0, False

Set objShell = Nothing