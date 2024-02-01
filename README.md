# Warning-Messenger-Bot
This is a bot for Telegram which allows personalized subscription to crisis warnings by the Federal Office of Civil Protection and Disaster Assistance for different locations.

## Description
This is a Telegram bot that retrieves population warnings through the NINA API of the Federal Office of Civil Protection and Disaster Assistance and conveys them using the Telegram API. The warnings are categorized into flood, weather, and civil protection, processed based on location and risk levels. Users can receive current warnings through queries or add subscriptions to be notified via push notifications about potential hazards. Additionally, users can request COVID-19 information for a specific location. Moreover, information on emergency preparedness and behaviour advice can be accessed and downloaded. The user-specific data stored by the bot can be deleted at any time.

The bot is controlled via text inputs and buttons in the Telegram chat, responding to users through the same chat.

The project was developed by PEASEC and a student group of the Technical University of Darmstadt to provide a Warning Messenger Bot for research purposes.

## Vorraussetzungen
- Python 3.9 is installed on the machine

## Installation
1. Clone the Git repository
2. Add a ```.env``` file at the top level
3. In the ```.env``` file, add the entry ```key = "Dein Telegram-Bot-Key"```
4. Install relevant packages with the command: ```pip install -r requirements.txt```

**Packages (see requirements.txt):**
- pyTelegramBotAPI==4.7.1
- python-decouple==3.6
- requests==2.28.1
- fuzzywuzzy~=0.18.0
- dataclasses~=0.6
- python-Levenshtein==0.20.9
- geopy~=2.3.0
- shapely==2.0.1
- mock~=5.0.1

## First initiation
1. Navigate to the folder ```\Warning-Messenger-Bot\source\```  through the command line
2. Execute the bot_runner.py file: ```pfad\zu\deiner\python\installation\python.exe bot_runner.py```
3. Search for the bot on Telegram (enter the bot's name or tag in the search bar) and press the “Start” button (or enter "/start") 
→ The bot immediately sends a message to initiate the chat

## <a name="head1234"></a>Configuration
- In the```.env ``` file, the token that the bot should use is set with ```key="BOT_TOKEN"```
- All texts sent by the bot are easily configurable in the file: ```text_templates.json```. A detailed explanation can be found in the file ```text_templates_manual.md```
- In the `config.json` file,  the following variables can be configured:
    - `subscription_timer_in_seconds` specifies the interval in seconds at which the current warnings, if not already sent, are sent to users with corresponding subscriptions
    - `warning_timer_in_seconds` specifies the interval in seconds at which, for the current warnings, if not already stored, the relevant postal codes are calculated and stored



## Details

### Internal states
![image](https://user-images.githubusercontent.com/118980413/222899837-139ba5fe-0111-4ade-8db3-807b1f0d7614.png)  
  
### Model overview
![image](https://user-images.githubusercontent.com/118980413/224966907-14614975-8076-42b7-aa6c-8fe97cf25bea.png)


The bot's start is managed through the ```bot_runner```. Running this creates three threads. In the first thread, the subscription mechanism runs, which by default checks every two minutes if new warnings need to be sent to the respective users. In the second thread, the ```receiver``` runs. It waits for user input in the Telegram chat and then calls the appropriate methods in the ```controller```. In the third thread, the ```warning_handler``` runs. It processes all active warnings upon the initial start of the bot and then scans for new warnings every two minutes by default. The ```controller``` then accesses various other modules, such as ```place_converter```, ```nina_service```, ```data_service```, ```text_templates``` and ```sender```. The ```sender``` then sends the chat message to the user. In the ```place_converter``` , suggestions for requested cities are generated. The ```nina_service``` serves as the interface to the NINA API, and the ```data_service``` represents the interface with our database. ```text_templates``` creates the appropriate text outputs (see [Configuration](#head1234)).

### Video Demo

WarningBot_demoVideo.gif
