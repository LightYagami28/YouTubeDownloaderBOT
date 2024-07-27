# YouTube Downloader Bot 🎥✨

A Telegram bot built using Node.js that allows you to download YouTube videos in various resolutions.

## Features 🌟

- Download YouTube videos in different resolutions
- Supports both YouTube links and short URLs (e.g., `https://youtu.be/`)
- Customizable emojis for the inline keyboard buttons
- Efficient file handling and temporary storage

## Installation 🛠️

### Prerequisites

Ensure you have Node.js installed. You can install Node.js by following the instructions at [nodejs.org](https://nodejs.org/en/download/).

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/youtube-downloader-bot.git
```

### 2. Navigate to the project directory:

```bash
cd youtube-downloader-bot
```

### 3. Install the required packages:

```bash
npm install
```

The required packages are listed in `package.json`.

### 4. Configure the bot:

Create a configuration file named `config.js` in the root of the project directory with the following content:

```javascript
module.exports = {
  botToken: 'YOUR_BOT_TOKEN',  // Your Bot Token
};
```

If you don't have a bot token, you can create a bot and obtain a token by following the [BotFather instructions](https://core.telegram.org/bots#botfather).

### 5. Run the bot:

```bash
node index.js
```

### 6. Interact with the bot:

1. Send a YouTube link to the bot.
2. Choose the desired resolution from the inline keyboard.
3. Wait for the bot to download and send the video.

## Download Links

- [Node.js Downloads](https://nodejs.org/en/download/) 

For specific OS installation instructions:

- **Windows:** Download the installer from the [Node.js website](https://nodejs.org/en/download/), run it, and follow the setup instructions.
- **macOS:** Use the [Node.js installer](https://nodejs.org/en/download/) or install via Homebrew with `brew install node`.
- **Linux:** Install using your distribution's package manager, e.g., `sudo apt install nodejs` for Debian-based distributions or `sudo dnf install nodejs` for Fedora.

By following these steps, you should be able to set up and run the YouTube Downloader Bot on your system.