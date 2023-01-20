import threading
import time

import receiver
import subscriptions

# Call this script to start the bot
def start_bot():
    """

    Starts the chat receiver and the subscription handling mechanism in two different threads

    """

    subscriptions_thread = threading.Thread(target=subscriptions.start_subscriptions)
    receiver_thread = threading.Thread(target=receiver.start_receiver)

    subscriptions_thread.start()
    receiver_thread.start()


start_bot()
