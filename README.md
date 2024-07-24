# YouTube Downloader Bot 🎥✨

A Telegram bot that allows you to download YouTube videos in various resolutions.

## Features 🌟

- Download YouTube videos in different resolutions
- Supports both YouTube links and short URLs (e.g., `https://youtu.be/`)
- Customizable emojis for the inline keyboard buttons
- Efficient file handling and temporary storage

## Installation 🛠️

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/youtube-downloader-bot.git
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   The required packages are:
   - `pyrogram`: A modern Telegram API client library for Python.
   - `pytube`: A lightweight, Pythonic, dependency-free, library for downloading YouTube videos.
   - `tgcrypto`: An optional package that significantly enhances the bot's speed.

3. Configure the bot:

   Update the following settings in the `config.py` file with your API keys:

   ```python
   api_id = 1  # Your API ID
   api_hash = ""  # Your API Hash
   bot_token = ""  # Your Bot Token
   ```

   If you don't have API keys, you can create an app to generate them [here](https://my.telegram.org/apps).

   You can also customize the emojis used in the bot by modifying the `EMOJIS` list in the `config.py` file.

## Usage 🚀

1. Start the bot:

   ```bash
   python main.py
   ```

2. Send a YouTube link to the bot.
3. Choose the desired resolution from the inline keyboard.
4. Wait for the bot to download and send the video.

## Contributing 🤝

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

When contributing, please ensure that you update the tests as appropriate.

## License 📄

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
