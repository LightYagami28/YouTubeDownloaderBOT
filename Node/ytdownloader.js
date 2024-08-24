const { exec } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { BOT_TOKEN } = require('./config');
const { Telegraf, Markup } = require('telegraf');

// Configurazione del bot
const bot = new Telegraf(BOT_TOKEN);
const EMOJIS = ["🔥", "🍬", "🌹", "🎂", "👀", "😜", "🎶"];
let videoLink = null;

// Creazione dei pulsanti di risoluzione per la tastiera inline
function createResolutionButtons(resolutions) {
  return Markup.inlineKeyboard(
    resolutions.map(resolution =>
      Markup.button.callback(`${getRandomEmoji()} ${resolution}`, resolution)
    )
  );
}

// Genera un'emoji casuale
function getRandomEmoji() {
  return EMOJIS[Math.floor(Math.random() * EMOJIS.length)];
}

// Scarica e invia il video
async function downloadAndSendVideo(ctx, link, resolution) {
  const videoPath = path.join(os.tmpdir(), 'video.mp4');
  
  try {
    await executeCommand(`youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' -o '${videoPath}' '${link}'`);
    await ctx.replyWithVideo({ source: videoPath }, { caption: '**Video scaricato con successo!**' });
  } catch (error) {
    console.error(`Errore durante il download del video: ${error}`);
    await ctx.reply('**Errore!** __Controlla la console.__');
  } finally {
    cleanUp(videoPath);
  }
}

// Esegui un comando shell
function executeCommand(command) {
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) {
        reject(error);
      } else {
        resolve(stdout);
      }
    });
  });
}

// Cancella il file scaricato
function cleanUp(filePath) {
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
  }
}

// Gestione del comando /start
bot.start((ctx) => ctx.reply('**Ciao!** __Mandami un link di YouTube!__'));

// Gestione dei messaggi di testo contenenti link di YouTube
bot.on('text', async (ctx) => {
  const text = ctx.message.text;
  if (text.includes('https://www.youtube.com/') || text.includes('https://youtu.be/')) {
    videoLink = text;
    const resolutions = ['720p', '480p', '360p', '240p', '144p'];
    await ctx.reply('Scegli una risoluzione:', createResolutionButtons(resolutions));
  }
});

// Gestione della selezione della risoluzione
bot.on('callback_query', async (ctx) => {
  const resolution = ctx.callbackQuery.data;
  await ctx.deleteMessage();
  await ctx.reply('Download in corso...');
  await downloadAndSendVideo(ctx, videoLink, resolution);
});

// Avvio del bot
bot.launch();
