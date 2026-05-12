Dim objShell
Set objShell = CreateObject("WScript.Shell")

objShell.Run "taskkill /F /IM pythonw.exe", 0, True

MsgBox "Don't Open my Privacy stopped.", 64, "Info"

Set objShell = Nothing