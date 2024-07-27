# YouTube Downloader Bot 🎥✨

A Telegram bot built using Go that allows you to download YouTube videos in various resolutions.

## Features 🌟

- Download YouTube videos in different resolutions
- Supports both YouTube links and short URLs (e.g., `https://youtu.be/`)
- Customizable emojis for the inline keyboard buttons
- Efficient file handling and temporary storage

## Installation 🛠️

### Prerequisites

Ensure you have Go installed. You can install Go by following the instructions at [golang.org/dl](https://golang.org/dl).

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
go mod tidy
```

The required packages are listed in `go.mod`.

### 4. Configure the bot:

Create a configuration file named `config.json` in the root of the project directory with the following content:

```json
{
  "bot_token": "YOUR_BOT_TOKEN"
}
```

If you don't have a bot token, you can create a bot and obtain a token by following the [BotFather instructions](https://core.telegram.org/bots#botfather).

### 5. Run the bot:

```bash
go run main.go
```

### 6. Interact with the bot:

1. Send a YouTube link to the bot.
2. Choose the desired resolution from the inline keyboard.
3. Wait for the bot to download and send the video.

## Download Links

- [Go Downloads](https://golang.org/dl/)

For specific OS installation instructions:

- **Windows:** Download the installer from the [Go website](https://golang.org/dl/), run it, and follow the setup instructions.
- **macOS:** Use the [Go installer](https://golang.org/dl/) or install via Homebrew with `brew install go`.
- **Linux:** Install using your distribution's package manager, e.g., `sudo apt install golang` for Debian-based distributions or `sudo dnf install golang` for Fedora.

By following these steps, you should be able to set up and run the YouTube Downloader Bot on your system.