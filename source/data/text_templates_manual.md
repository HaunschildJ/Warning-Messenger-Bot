## Anleitung, wie man die Schablonen in TextTemplates.json benutzt und anpasst

In TextTemplates.json liegen die Schablonen, mit denen man den Text anpassen kann, mit dem
die von der NINA API geholten Informationen präsentiert werden. Hier finden sich auch die Beschriftungen der Knöpfe,
die der Bot verwendet, um dem Nutzer eine angenehmere Usability zu gewährleisten.

Die json ist ein Array von dictionaries. Die Felder `"description":` stehen immer für eine Erklärung und werden vom Bot ignoriert.
Alle ausgaben des Bots können mit HTML-Tags versehen werden. 

Der erste Eintrag `"topic": "replaceable_answers"` stellt die Antworten dar, 
welche mit Inhalt (meist aus der NINA API) befüllt werden. Dieser Eintrag ist so aufgebaut, dass in `"all_answers":` alle 
Antworten dieser Kategorie als Array von dictionaries stehen. Innerhalb der jeweiligen Antwort steht `"topic":` für den Namen, 
welcher innerhalb des Codes verwendet wird und `"information":` für den Text, welchen der Bot ausgibt. Hierbei werden bei 
allen Einträgen des Arrays die `"text":` Felder genommen und mit \n der Reihenfolge nach aneinander gereiht.
Es sollten nur die Felder nach `"text":` verändert werden.

Der zweite Eintrag `"topic": "buttons"` speichert in dem dictionary nach `"names":` die Button-Namen für den Bot. Beispiel:
`"settings": "Einstellungen ⚙️"` hierbei steht `settings` für den Namen des Knopfes innerhalb des Codes und sollte daher 
nicht verändert werden. `Einstellungen ⚙️` steht für den Namen des Knopfes, welcher im Telegram Chat angezeigt wird. 
Dieser kann ohne Probleme verändert werden.

Der dritte Eintrag `"topic": "answers"` stellt die einfachen Antworten des Bots bereit.
Innerhalb des dictionaries nach `"text":` werden alle einfachen Antworten gespeichert in der gleichen Form wie bei den Knöpfen (zweiter Eintrag).

Der vierte Eintrag `"topic": "complex_answers"` stellt die komplexen Antworten des Bots bereit.
Hierbei werden wieder in dem dictionary nach `"all_answers"` alle Antworten gespeichert. 
Ähnlich wie bei den beiden vorherigen Einträgen ist auch hier zum Beispiel `"show_subscriptions:"` der Name, welcher im 
Code verwendet wird und das dictionary dahinter stellt die Antwort dar.
Da diese, wie der Name schon sagt, komplex sind, ist hier die Beschreibung in "description" zu verwenden.

- In 1) wird beschrieben, wie man die Texte ändern kann.
- In 2) wird beschrieben, wie man neue Buttons/ Knöpfe hinzufügen kann.
- In 3) wird beschrieben, wie andere Programmierer die Datei nutzen können.
---
### 1. Anpassung

#### NINA API

Man öffnet die Datei TextTemplates.json mit einem beliebigen Text-Editor.
Man sucht mit Strg + F nach `"topic":` und stößt auf alle Themen, deren Texte man ändern kann.
Beispielhaft seien hier covid_info und covid_rules genannt. Antworten die Inhalte der NINA API beinhalten
sind in den `"topic": "replaceable_answers"` (erster Eintrag) und `"topic": "complex_answers"` (vierter Eintrag)
zu finden.

Hat man so zum gewünschten Thema navigiert, kann man die darunter folgenden Blöcke anpassen.

Die `"description":` zeigt auf, an welche Stelle man seinen Text schreiben kann. Das Muster ist immer gleich:
Man kann alles ändern, was nach `"text"` oder, wie dann in description beschrieben, einem anderen Namen folgt und muss dabei nur eine Einschränkung beachten:

Das `%Beispiel` sollte nicht vollends entfernt werden. Das wird später nämlich mit den Daten ersetzt, die von der
NINA API kommen. Man hat freie Wahl, wohin man das setzt, aber es muss vorhanden sein.

#### Buttons/ einfache Antworten

Möchte man den Text bestehender Buttons ändern, muss man an die Stelle der TextTemplates.json Datei navigieren, wo
`"topic": "buttons"` (zweiter Eintrag) steht.

Dort ändert man den Text des gewünschten Buttons, indem man den Text *nach* dem Doppelpunkt anpasst.

Für einfache Antworten navigiert man zu `"topic": "answers"` (dritter Eintrag). Ansonsten analog zu Buttons.

---
### 2. Neue Buttons/einfache Antworten hinzufügen

Möchte man neue **Buttons** hinzufügen, muss man an die Stelle der text_templates.json Datei navigieren, wo
`"topic": "buttons"` steht.

Dort fügt man eine neue Zeile hinzu. Das Muster lautet:

`"internerButtonName" : "gewünschterButtonText"`

Man beachte, dass jede Zeile, außer die letzte, mit einem Komma enden muss.

Der interne Button Name muss in der Datei enum_types.py in der Enum-Klasse "Button" hinzugefügt werden um ihn dann im Code
nutzen zu können.

`NAME_DES_BUTTONS = "internerButtonName"`

Für **einfache Antworten** ("topic": "answers") ist der Prozess gleich bis auf die Klasse in enum_types.py. Hierbei muss man 
die Enum-Klasse "Answers" nehmen.



---
### 3. Nutzung

Die Enums sind alle in enum_types.py gespeichert.

#### Ersetzbare Antworten

Für die ersetzbaren Antworten muss für jede neue Antwort eine neue Methode in text_templates.py implementiert werden.
Hierbei nutzt man die Methode `get_replaceable_answer` mit dem Enum `ReplaceableAnswer` für die gewünschte Antwort und 
ersetzt dann alle `%Beispiel` mit den gewünschten Texten. Analog für die komplexen Antworten mit `_get_complex_answer_dict`
und als Parameter der interne Name der Antwort als String.
Alle Methoden müssen einen String zurückgeben, welcher dann die Antwort für den Bot beinhaltet.

#### Buttons und einfache Antworten

Für die Buttons gibt es die Methode `get_button_name` mit dem gewünschten Button in From des Enums `Button` als Parameter.
Für die einfachen Antworten gilt analog die Methode `get_answers` und das Enum `Answers`. 

Beide Methoden geben in Form eines Strings den gewünschten Text zurück. 