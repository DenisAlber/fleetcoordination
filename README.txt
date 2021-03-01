1. Lösche alle vorhanden Ordner und Dateien in VSCode die nichts mit dem eigentlichen Projekt zu tun haben (z. B. .vscode, .venv etc..) außer der .gitignore
2. Im Terminal "py -m venv .venv" eingeben und bestätigen und ggf. PopUp bestätigen
3. Mit "Strg + Shift + P" Auswahlfenster öffnen und "Python: Select Interpreter" auswählen und darunter dann "Python 3.9.x 64-bit ('.venv')" auswählen
4. Unter Terminal -> New Terminal neues Terminal öffnen.
5. Wenn ein Error im neuen Terminal erscheint: Windows PowerShell als Admin starten -> "Set-ExecutionPolicy Unrestricted" eingeben und mit "y" bestätigen
6. VS Code neu starten, nochmals den Interpreter in Punkt 3 auswählen und neues Terminal starten (Fehler dürfte nun nicht mehr erscheinen)
7. Im Terminal müsste nun vor dem Pfad "(.venv)" in grüner Schrift stehen. Jetzt noch mit "py -m pip install py-linq" py-linq darin installieren
8. Testen ob alles funktioniert, wenn im das Module "six" fehlt einfach noch mit "py -m pip install six" installieren