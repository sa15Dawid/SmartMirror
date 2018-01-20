# SmartMirror

Dieser Smart Mirror wurde Python und mittels des daugehörigen Bindings PyQt5 umgesetzt. Die auf diese Weise erstellte GUI (graphical user interface) und alle anderen dazugehörigen Programme werden auf einen Raspberry Pi 3 Modell B ausgeführt. Dieser ist das Herzstück und überträgt das Bild auf den Display, der in diesem Fall ein Pi-Top ist.
Benötigte Komponenten:

  * Raspberry Pi (3 Modell B)
  * Display (je nach Anforderung wählbar)
  * HDMI – Kabel
  * Einwegspiegel oder Einwegspiegelfolie (frei Wählbar. Funktioniert unterschiedlich gut.)

Die mit PyQt5 erstellte Benutzeroberfläche wird in drei Teile aufsplittetet. Diese bestehen aus eine Startfenster, welches dem Benutzer neben der aktuellen Uhrzeit und dem Datum,  die Temperatur anzeigt. Zusätzlich wird noch ein Zitat eingeblendet. 
Das zweite Fenster, welches das Wetter genauer präsentiert, besteht aus dem angezeigtem Ort, also Stadt und Land. Diese Seite zeigt auch die voraussichtlichen Zeiten des Sonnenuauf- und Sonnenuntergangs an, die Höchst- und Tiefsttemperatur und auch eine Wettervorhersage für die nächsten fünf Tage.
Zum Schluss noch das letzte letzte Fenster, welches für die Anzeige der intelligenten Geräte ausgelegt wurde. Hier werden die Geräte, die in der hier verwendeten Automatisierungssoftware, eingebunden sind, in einer Liste, samt Namen und Status, angezeigt. Beim Schalten der Geräte, zum Beispiel der Lichtquellen wir der Zustand sofort auf der Anzeige aktualisiert.

Nun zur verwendeten Software:

  * openHAB 2 – eine Haus- und Gebäudeautomatisierungs- Open Source Software
  * Bottle – ein schnelles, einfaches und leichtgewichtiges WSGI micro web-framework für Python
  * Python
  * PyQt5
  
Um das Programm auszuführen, das Git Repository clonen, danach alle fehlenden, wenn nicht bereits vorhandenen Bindings und Erweiterungen, downloaden und installieren. Die GUI wird gestartet, wenn das Python Script "SmartMirror.py" ausgeführt wird. Dieses kann in der Ordnerstruktur SmartMirror/src/PyQt5/SmartMirror.py gefunden werden. 
Die restlichen Dateien in diesem Ordner wurden zu Versuchszwecken verwendet.

Weiters können im Ordner SmartMirror/src/OpenHAB alle notwendigen Dateien gefunden werden, die für die richtige Funktonsweise benötigt werden. Dazu werden die Ordner kopiert und bei dem Verzeichnis von Openhab (meist /etc/openhab2/...) die bereits vorhandenen ersetzt.

Zuletzt muss noch die Api beim Systemstart automatisch gestartet werden, dazu die das Shell Script in SmartMirror/src/API/Api.sh mit dem Hochfahren des Rechners gestartet.
