const { exec } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { BOT_TOKEN } = require('./config');
const { Telegraf, Markup } = require('telegraf');


// Configuration
const bot = new Telegraf(BOT_TOKEN);
let LINK = null;
const EMOJIS = ["🔥", "🍬", "🌹", "🎂", "👀", "😜", "🎶"];

// Create resolution buttons for inline keyboard
function createResolutionButtons(resolutions) {
  return Markup.inlineKeyboard(
    resolutions.map((res) => Markup.button.callback(`${EMOJIS[Math.floor(Math.random() * EMOJIS.length)]} ${res}`, res))
  );
}

// Download and send video
async function downloadAndSendVideo(ctx, link, resolution) {
  try {
    const videoPath = path.join(os.tmpdir(), 'video.mp4');
    await new Promise((resolve, reject) => {
      exec(`youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' -o '${videoPath}' '${link}'`, (error, stdout, stderr) => {
        if (error) {
          reject(error);
        } else {
          resolve();
        }
      });
    });
    await ctx.replyWithVideo({ source: videoPath }, { caption: '**Video downloaded!**' });
    fs.unlinkSync(videoPath);
  } catch (e) {
    console.error(`Error downloading video: ${e}`);
    await ctx.reply('**Error!** __Check console.__');
  }
}

// Start command
bot.start((ctx) => ctx.reply('**Hello!** __Send me a YouTube link!__'));

// Handle YouTube link
bot.on('text', async (ctx) => {
  if (ctx.message.text.includes('https://www.youtube.com/') || ctx.message.text.includes('https://youtu.be/')) {
    LINK = ctx.message.text;
    const resolutions = ['720p', '480p', '360p', '240p', '144p'];
    await ctx.reply('Pick a resolution:', createResolutionButtons(resolutions));
  }
});

// Handle resolution selection
bot.on('callback_query', async (ctx) => {
  const resolution = ctx.callbackQuery.data;
  await ctx.deleteMessage();
  await ctx.reply('Downloading...');
  await downloadAndSendVideo(ctx, LINK, resolution);
});

bot.launch();
