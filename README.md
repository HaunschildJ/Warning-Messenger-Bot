# Warning-Messenger-Bot
Dieser Bot ist Teil des Bachelorpraktikum-Projekts 2022/23 der TU Darmstadt.

## Beschreibung
Dies ist ein Telegram-Bot, der Bevölkerungswarnungen über die NINA API abrufen und über die Telegram API vermitteln kann. 
Die Warnungen sind den Kategorien Hochwasser, Wetter und Bevölkerungsschutz  zugeordnet und Standort- und Risikostufen-abhängig verarbeitet. Nutzer:innen können per Abfrage aktuelle Warnungen erhalten oder Abonnements hinzufügen, um per Push-Benachrichtigung über Gefahren informiert zu werden. 
Außerdem kann man bei Bedarf Corona-Informationen über einen Standort abfragen.
Darüber hinaus können Informationen zu Verhaltenshinweisen in Notfällen abgerufen werden. Die nutzerbezogenen Daten, welche der Bot speichert, können jederzeit gelöscht werden.
Der Bot wird über Texteingaben und Buttons im Telegram-Chat gesteuert und antwortet Nutzer:innen über selbigen Chat.

Das Projekt wurde im Auftrag von PEASEC erstellt, um einen Warning Messenger Bot als konkretes Beispiel für die Forschung, also z.B. Umfragen (aktuell z.B. um sich ein Bild zu machen, ob die Bevölkerung einen Warn-Bot nutzen würde bzw. er eine gute Alternative zu den Warn-Apps darstellt), zu haben.

## Vorraussetzungen
- Python 3.9 ist auf der Maschine installiert

## Installation

1. Git Repository klonen
2. ```.env``` Datei auf oberster Ebene hinzufügen
3. In die in 2. erstellte Datei ```key = "Dein Telegram-Bot-Key"``` schreiben
4. Relevante Packages installieren (siehe unten) ```pip install -r requirements.txt```
Packages (siehe requirements.txt):
- pyTelegramBotAPI==4.7.1
- python-decouple==3.6
- requests==2.28.1
- fuzzywuzzy~=0.18.0
- dataclasses~=0.6
- python-Levenshtein==0.20.9
- geopy~=2.3.0
- shapely==2.0.1
- mock~=5.0.1

## Erster Start
1. Über die Kommandozeile in den Ordner ```\Warning-Messenger-Bot\source\``` navigieren
2. bot_runner.py Datei ausführen: ```python3 bot_runner.py```
3. Den Bot über Telegram suchen (Name oder Tag des Bots in der Suchleiste eingeben) und auf den “Start” Knopf drücken (oder "/start" eingeben) 
→ der Bot schickt direkt eine Nachricht zur Einleitung des Chats

## Konfigurationsoptionen
- token
- Alle Texte, welche der Bot sendet, sind leicht konfigurierbar in der Datei: ```text_templates.json```

## Detail-Informationen
![image](https://user-images.githubusercontent.com/118980413/222899837-139ba5fe-0111-4ade-8db3-807b1f0d7614.png)

Module Erklärt:
![image](https://user-images.githubusercontent.com/118980413/224966907-14614975-8076-42b7-aa6c-8fe97cf25bea.png)


