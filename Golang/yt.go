package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"

	"github.com/go-telegram-bot-api/telegram-bot-api"
)

type config struct {
	BotToken string `json:"bot_token"`
}

func main() {
	// Carica la configurazione dal file
	configFile, err := os.Open("config.json")
	if err != nil {
		log.Fatal(err)
	}
	defer configFile.Close()

	var cfg config
	err = json.NewDecoder(configFile).Decode(&cfg)
	if err != nil {
		log.Fatal(err)
	}

	// Crea il bot
	bot, err := tgbotapi.NewBotAPI(cfg.BotToken)
	if err != nil {
		log.Fatal(err)
	}

	var link string
	emojis := []string{"🔥", "🍬", "🌹", "🎂", "👀", "😜", "🎶"}

	// Create resolution buttons for inline keyboard
	createResolutionButtons := func(resolutions []string) tgbotapi.InlineKeyboardMarkup {
		buttons := make([]tgbotapi.InlineKeyboardButton, len(resolutions))
		for i, res := range resolutions {
			emoji := emojis[i%len(emojis)]
			buttons[i] = tgbotapi.NewInlineKeyboardButtonData(fmt.Sprintf("%s %s", emoji, res), res)
		}
		return tgbotapi.NewInlineKeyboardMarkup(buttons)
	}

	// Download and send video
	downloadAndSendVideo := func(chatID int64, link, resolution string) {
		videoPath := filepath.Join(os.TempDir(), "video.mp4")
		cmd := exec.Command("youtube-dl", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", "-o", videoPath, link)
		if err := cmd.Run(); err != nil {
			fmt.Println("Error downloading video:", err)
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

	// Start command
	bot.Handle("/start", func(update *tgbotapi.Update) {
		msg := tgbotapi.NewMessage(update.Message.Chat.ID, "*Hello!* __Send me a YouTube link!__")
		msg.ParseMode = "markdown"
		bot.Send(msg)
	})

	// Handle YouTube link
	bot.Handle(tgbotapi.UpdateTypeMessage, func(update *tgbotapi.Update) {
		text := update.Message.Text
		if strings.Contains(text, "https://www.youtube.com/") || strings.Contains(text, "https://youtu.be/") {
			link = text
			resolutions := []string{"720p", "480p", "360p", "240p", "144p"}
			msg := tgbotapi.NewMessage(update.Message.Chat.ID, "Pick a resolution:")
			msg.ReplyMarkup = createResolutionButtons(resolutions)
			bot.Send(msg)
		}
	})

	// Handle resolution selection
	bot.Handle(tgbotapi.UpdateTypeCallbackQuery, func(update *tgbotapi.Update) {
		resolution := update.CallbackQuery.Data
		chatID := update.CallbackQuery.Message.Chat.ID
		bot.AnswerCallbackQuery(tgbotapi.NewCallback(update.CallbackQuery.ID, ""))
		bot.DeleteMessage(tgbotapi.DeleteMessageConfig{
			ChatID:    chatID,
			MessageID: update.CallbackQuery.Message.MessageID,
		})
		msg := tgbotapi.NewMessage(chatID, "Downloading...")
		bot.Send(msg)
		downloadAndSendVideo(chatID, link, resolution)
	})

	bot.Receive()
}
