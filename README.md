# YOUTUBE DOWNLOADER BOT 🎆

A bot finalized to download YouTube Links using PyTube's Python Library.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following packages.

```bash
pip install pyrogram, pytube, tgcrypto
```
The packages are needed to make the bot work properly.
TgCrypto is "optional", however it would make the bot signficantly faster.

Change the following settings:
```python
api_id = 1 #YOUR API ID
api_hash = "" #YOUR API KEY
bot_token = "" #YOUR BOT TOKEN
```
Into your API keys, if you don't have API keys you can create an App to generate them [here](https://my.telegram.org/apps).

You can also change the random emojis choosen in this list (or add other ones):
```python
EMOJIS = ["🔥","🍬","🌹","🎂","👀","😜","🎶"]
# Example: EMOJIS = ["🔥","🍬","🌹","🎂","👀","😜","🎶", "🤷‍♀️","🎉💕"]
```

## Usage

You start the bot, and send a youtube link, choose the resolution and wait for the bot to send you the video!

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
