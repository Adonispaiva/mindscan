Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\Backup MindScan.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "D:\projetos-inovexa\mindscan\backup_mindscan.bat"
oLink.WindowStyle = 1
oLink.IconLocation = "cmd.exe, 0"
oLink.Save
