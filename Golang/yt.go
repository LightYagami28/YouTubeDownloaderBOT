package main

import (
    "encoding/json"
    "fmt"
    "log"
    "os"
    "os/exec"
    "path/filepath"
    "strings"

    tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
)

type Config struct {
    BotToken string `json:"bot_token"`
}

func loadConfig(filePath string) (*Config, error) {
    var config Config
    file, err := os.Open(filePath)
    if err != nil {
        return nil, err
    }
    defer file.Close()

    decoder := json.NewDecoder(file)
    if err := decoder.Decode(&config); err != nil {
        return nil, err
    }
    return &config, nil
}

func createResolutionButtons(resolutions []string, emojis []string) tgbotapi.InlineKeyboardMarkup {
    buttons := make([]tgbotapi.InlineKeyboardButton, len(resolutions))
    for i, res := range resolutions {
        emoji := emojis[i%len(emojis)]
        buttons[i] = tgbotapi.NewInlineKeyboardButtonData(fmt.Sprintf("%s %s", emoji, res), res)
    }
    return tgbotapi.NewInlineKeyboardMarkup(buttons)
}

func downloadAndSendVideo(bot *tgbotapi.BotAPI, chatID int64, link string, resolution string) {
    videoPath := filepath.Join(os.TempDir(), "video.mp4")
    cmd := exec.Command("youtube-dl", "-f", resolution, "-o", videoPath, link)
    if err := cmd.Run(); err != nil {
        log.Printf("Error downloading video: %v", err)
        msg := tgbotapi.NewMessage(chatID, "*Error!* __Check console.__")
        msg.ParseMode = "markdown"
        bot.Send(msg)
        return
    }

    video := tgbotapi.NewVideoUpload(chatID, videoPath)
    video.Caption = "*Video downloaded!*"
    video.ParseMode = "markdown"
    bot.Send(video)
    os.Remove(videoPath)
}

func handleUpdate(bot *tgbotapi.BotAPI, update tgbotapi.Update, emojis []string) {
    if update.Message == nil {
        return
    }

    if update.Message.Text == "/start" {
        msg := tgbotapi.NewMessage(update.Message.Chat.ID, "*Hello!* __Send me a YouTube link!__")
        msg.ParseMode = "markdown"
        bot.Send(msg)
    } else if strings.Contains(update.Message.Text, "https://www.youtube.com/") || strings.Contains(update.Message.Text, "https://youtu.be/") {
        link := update.Message.Text
        resolutions := []string{"720p", "480p", "360p", "240p", "144p"}
        msg := tgbotapi.NewMessage(update.Message.Chat.ID, "Pick a resolution:")
        msg.ReplyMarkup = createResolutionButtons(resolutions, emojis)
        bot.Send(msg)
    } else if update.CallbackQuery != nil {
        resolution := update.CallbackQuery.Data
        chatID := update.CallbackQuery.Message.Chat.ID
        bot.AnswerCallbackQuery(tgbotapi.NewCallback(update.CallbackQuery.ID, ""))
        bot.DeleteMessage(tgbotapi.DeleteMessageConfig{
            ChatID:    chatID,
            MessageID: update.CallbackQuery.Message.MessageID,
        })
        msg := tgbotapi.NewMessage(chatID, "Downloading...")
        bot.Send(msg)
        downloadAndSendVideo(bot, chatID, link, resolution)
    }
}

func main() {
    // Load configuration
    config, err := loadConfig("config.json")
    if err != nil {
        log.Fatalf("Error loading config: %v", err)
    }

    // Create bot
    bot, err := tgbotapi.NewBotAPI(config.BotToken)
    if err != nil {
        log.Fatalf("Error creating bot: %v", err)
    }
    log.Printf("Authorized on account %s", bot.Self.UserName)

    // Emojis for resolution buttons
    emojis := []string{"🔥", "🍬", "🌹", "🎂", "👀", "😜", "🎶"}

    // Create update channel
    u := tgbotapi.NewUpdate(0)
    u.Timeout = 60
    updates := bot.GetUpdatesChan(u)

    // Process updates
    for update := range updates {
        handleUpdate(bot, update, emojis)
    }
}
