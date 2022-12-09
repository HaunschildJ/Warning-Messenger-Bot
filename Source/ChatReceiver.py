import Bot
import Controller
from Controller import Commands
from Controller import ErrorCodes

bot = Bot.bot

# filter for message handlers ------------------------------------------------------------------------------------------


def filter_corona(message) -> bool:
    if message.text.split(' ')[0] == Commands.CORONA.value:
        return True
    return False


def filter_callback_corona(call) -> bool:
    if call.data.split(' ')[0] == Commands.CORONA.value:
        return True
    return False

# bot message handlers -------------------------------------------------------------------------------------------------


@bot.message_handler(commands=['start'])
def start(message):
    """
    This method is called when the user sends '/start' (mainly for the start of the conversation with the bot)
    and will then initiate the chat with the user by calling start in Controller

    Arguments:
        message: the message that the user sent in the chat
    Returns:
        Nothing
    """
    Controller.start(message.chat.id)


@bot.message_handler(func=filter_corona)
def corona(message):
    """
    This method is called when the user sends Commands.CORONA.value (currently '/corona') and will call the methods
    needed to give the user the desired output
    """
    corona_helper(message.chat.id, message.text)


@bot.message_handler(regexp="Corona Infos")
def corona_with_inline_buttons(message):
    """
    When 'Corona Infos' is sent in a chat this method gets called (mainly for the keyboard buttons) and will then
    call the method to show the corresponding inline buttons in the chat

    Arguments:
        message: the message that the user sent in the chat
    Returns:
        Nothing
    """
    Controller.show_inline_button(message.chat.id, Controller.ButtonType.CORONA_INFO)


@bot.message_handler(regexp="Corona Rules")
def corona_with_inline_buttons(message):
    """
    When 'Corona Rules' is sent in a chat this method gets called (mainly for the keyboard buttons) and will then
    call the method to show the corresponding inline buttons in the chat

    Arguments:
        message: the message that the user sent in the chat
    Returns:
        Nothing
    """
    Controller.show_inline_button(message.chat.id, Controller.ButtonType.CORONA_RULES)


# bot callback handlers ------------------------------------------------------------------------------------------------


@bot.callback_query_handler(func=filter_callback_corona)
def corona_button(call):
    """
    This method is a callback_handler for the corona inline buttons and will call the methods needed to give the user
    the desired output \n
    It will also delete the inline buttons

    Arguments:
        call: Data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    corona_helper(chat_id, call.data)
    Controller.delete_message(chat_id, call.message.id)


# helper methods -------------------------------------------------------------------------------------------------------


def corona_helper(chat_id, message_string):
    """
    This is a helper method for the user input handlers above \n
    With the message/text the user/button sent (message_string) this method will then call the corresponding method in
    Controller so that the desired output will be sent to the user

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        message_string: a string of the message/text that is sent by the user/button
    Returns:
        Nothing
    """
    split_message = message_string.split(' ')
    if split_message[1] == Commands.CORONA_INFO.value:
        Controller.corona_info(chat_id, split_message[2])
    elif split_message[1] == Commands.CORONA_RULES.value:
        Controller.corona_rules(chat_id, split_message[2])
    else:
        Controller.error_handler(chat_id, ErrorCodes.ONLY_PART_OF_COMMAND)


bot.polling()

