## Anleitung, wie man die Schablonen in TextTemplates.json benutzt und anpasst

In TextTemplates.json liegen die Schablonen, mit denen man den Text anpassen kann, mit dem
die von der NINA API geholten Informationen präsentiert werden. Hier finden sich auch die Beschriftungen der Knöpfe,
die der Bot verwendet, um dem Nutzer eine angenehmere Usability zu gewährleisten.

- In 1) wird beschrieben, wie man die Texte ändern kann.
- In 2) wird beschrieben, wie man neue Buttons/ Knöpfe hinzufügen kann.
- In 3) wird beschrieben, wie andere Programmierer die Datei nutzen können.
---
1. ### Anpassung

#### NINA API

Man öffnet die Datei TextTemplates.json mit einem beliebigen Text-Editor.
Man sucht mit Strg + F nach "topic" und stößt auf alle Themen, deren Texte man ändern kann.
Beispielhaft seien hier covid_info und covid_rules genannt.

Hat man so zum gewünschten Thema navigiert, kann man die darunter folgenden Blöcke anpassen.

Die "description" zeigt auf, an welche Stelle man seinen Text schreiben kann. Das Muster ist immer gleich:
Man kann alles ändern, was nach "text" folgt und muss dabei nur eine Einschränkung beachten:

Das "%Beispiel" darf nicht vollends entfernt werden. Das wird später nämlich mit den Daten ersetzt, die von der
NINA API kommen. Man hat freie Wahl, wohin man das setzt, aber es muss vorhanden sein.

#### Buttons

Möchte man den Text bestehender Buttons ändern, muss man an die Stelle der TextTemplates.json Datei navigieren, wo
"topic": "buttons" steht.

Dort ändert man den Text des gewünschten Buttons, indem man den Text *nach* dem Doppelpunkt anpasst.

---
2. ### Neue Buttons hinzufügen

Möchte man neue Buttons hinzufügen, muss man an die Stelle der TextTemplates.json Datei navigieren, wo
"topic": "buttons" steht.

Dort fügt man eine neue Zeile hinzu. Das Muster lautet:

"internerButtonName" : "gewünschterButtonText"

Man beachte, dass jede Zeile, außer die letzte, mit einem Komma enden muss.

---
3. ### Nutzung

#### NINA API

Anlaufpunkt ist die Methode get_topic_info(..) in TextTemplates.py. Sie ist dank eines Enums so implementiert,
dass man sie nur mit gültigen Werten als Parameter aufrufen kann.

Sie gibt einen String zurück, in dem die gewünschten Informationen mit Absätzen
getrennt aneinander gehängt wurden.

#### Buttons

Analog für die Buttons. Nur hier heißt die Methode get_button_name(..).