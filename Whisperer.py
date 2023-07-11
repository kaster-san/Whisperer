import argparse
import asyncio
import configparser
import logging
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import *
import time

# Argument Parser
parser = argparse.ArgumentParser(description="UnseenChatTracker")
parser.add_argument("-e", "--excluded-groups", nargs="+", type=int, default=[], help="List of excluded group IDs")
parser.add_argument("-f", "--file", type=str, default="unseen_messages.txt", help="File name to store the message")
args = parser.parse_args()

# Retrieve API ID and API hash from the .config file or user input
config = configparser.ConfigParser()

# Create the 'Telegram' section if it doesn't exist
if 'Telegram' not in config.sections():
    config['Telegram'] = {}

config.read(".config")
api_id = config.get("Telegram", "API_ID", fallback="")
api_hash = config.get("Telegram", "API_HASH", fallback="")

if not api_id:
    api_id = input("Enter your API ID: ")
    config.set("Telegram", "Telegram", api_id)
if not api_hash:
    api_hash = input("Enter your API hash: ")
    config.set("Telegram", "API_HASH", api_hash)

with open(".config", "w") as configfile:
    config.write(configfile)

# Validate API ID and API hash
if not api_id.isdigit() or not api_hash.isalnum():
    raise ValueError("Invalid API ID or API hash. Please check your input.")

# List of excluded group IDs
excluded_group_ids = args.excluded_groups

# Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Prompt the user to enter the message
message = input("Enter the message you want to send: ")
time_sleep = float(input("Enter the time sleep value (in seconds): "))

# Create the client
client = TelegramClient('session_name', api_id, api_hash)

# Start the client
client.start()

# Get all the dialogs (conversations)
dialogs = client.loop.run_until_complete(client.get_dialogs())


# Asynchronous function to send messages
async def send_messages():
    # Loop through the dialogs and send the message to all groups except the excluded ones
    for dialog in dialogs:
        if dialog.is_group and dialog.entity.id not in excluded_group_ids:
            try:
                if dialog.entity.slowmode_seconds > 0:
                    continue  # Skip this group if it has slow mode enabled
            except AttributeError:
                pass  # Skip this group if it's not a group (i.e., it's a channel)

            try:
                await client.send_message(dialog.id, message, silent=True)
                logging.info(f"Message sent successfully to group {dialog.entity.title}")
            except ChatWriteForbiddenError as e:
                logging.warning(f"Skipping group {dialog.entity.title} due to write permissions: {e}")
            except SlowModeWaitError as e:
                # Calculate the required wait time
                wait_time = e.seconds
                logging.info(f"Slow mode active, waiting for {wait_time} seconds...")
            except FloodWaitError as e:
                logging.warning(f"Waiting {e.seconds} seconds before sending another message")
                await asyncio.sleep(e.seconds)
            except ChatWriteForbiddenError as e:
                logging.warning(f"Cannot send messages to {dialog.name}: {e}")
            except PeerIdInvalidError as e:
                logging.warning(f"Invalid peer {dialog.name}: {e}")
            except UserBannedInChannelError as e:
                logging.warning(f"You are banned from {dialog.entity.title}: {e}")
            except Exception as e:
                logging.error(f"Error occurred while sending message to group {dialog.entity.title}: {type(e).__name__}: {e}")
                continue
             # Sleep for the specified time
            await asyncio.sleep(time_sleep)

# Create the event loop
loop = asyncio.get_event_loop()

# Run the asynchronous function in the event loop
loop.run_until_complete(send_messages())

# Store the message in the specified file
with open(args.file, "w", encoding='utf-8') as file:
    file.write(message)