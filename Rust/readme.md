# YouTube Downloader Bot 🎥✨

A Telegram bot built using Rust that allows you to download YouTube videos in various resolutions.

## Features 🌟

- Download YouTube videos in different resolutions
- Supports both YouTube links and short URLs (e.g., `https://youtu.be/`)
- Customizable emojis for the inline keyboard buttons
- Efficient file handling and temporary storage

## Installation 🛠️

### Prerequisites

Ensure you have Rust installed. You can install Rust by following the instructions at [rustup.rs](https://rustup.rs/).

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/youtube-downloader-bot.git
```

### 2. Navigate to the project directory:

```bash
cd youtube-downloader-bot
```

### 3. Build the project:

```bash
cargo build --release
```

### 4. Configure the bot:

Create a configuration file named `config.txt` in the root of the project directory with the following content:

```
bot_token=YOUR_BOT_TOKEN  # Your Bot Token
```

If you don't have a bot token, you can create a bot and obtain a token by following the [BotFather instructions](https://core.telegram.org/bots#botfather).

### 5. Run the bot:

```bash
cargo run --release
```

### 6. Interact with the bot:

1. Send a YouTube link to the bot.
2. Choose the desired resolution from the inline keyboard.
3. Wait for the bot to download and send the video.