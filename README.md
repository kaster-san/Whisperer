# Whisperer

Whisperer is a Python script that allows you to send messages to multiple groups on Telegram. It leverages the power of the Telethon library to send messages discreetly and efficiently.

## Features

- Send messages to multiple Telegram groups simultaneously.
- Exclude specific groups from receiving the message.
- Specify the time interval between sending messages to groups.
- Error handling for various exceptions during the message sending process.
- Logging of important events and errors.

## Requirements

- Python 3.x or higher
- Telethon library (`pip install telethon`)

## Usage

1. Make sure you have Python installed on your system.

3. Install the required dependencies by running `pip install telethon`.
   
4. Obtain the API ID and API hash from the Telegram website by creating a new application.
   
5. Run the script using the following command:
   `python whisperer.py -e <excluded-groups> -f <file-name>`
- Replace `<excluded-groups>` with a space-separated list of group IDs to exclude (optional), and `<file-name>` with the desired name for the message storage file (optional, default is `unseen_messages.txt`).

7. Follow the instructions prompted by the script to enter the message you want to send and the time interval between sending messages.

8. Sit back and let Whisperer do the work!
   
## **Disclaimer**: 
The use of Whisperer for sending messages should comply with Telegram's terms of service. Ensure that you have the necessary permissions to send messages to the target groups. The developers of Whisperer are not responsible for any misuse or violations of Telegram's terms of service that may result from the use of this script.

**Note**: Ensure that you have the necessary permissions to send messages to the target groups. The script will handle any exceptions related to group permissions and slow mode.

## Limitations

- Sending large volumes of messages or spamming groups may lead to temporary restrictions on your Telegram account. Use the script responsibly and in accordance with Telegram's terms of service.

## Contributing

Contributions, bug reports, and feature requests are welcome! If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the GPLv2 License. See the [LICENSE](LICENSE) file for more details.


   
