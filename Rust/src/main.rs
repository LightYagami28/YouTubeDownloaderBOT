use std::env;
use std::error::Error;
use std::fs;
use std::path::PathBuf;
use std::process::Command;
use teloxide::{prelude::*, utils::command::BotCommand};

#[derive(BotCommand)]
#[command(rename = "start")]
struct Start;

#[derive(BotCommand)]
#[command(rename = "download")]
struct Download {
    link: String,
    resolution: String,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error + Send + Sync>> {
    let bot = Bot::from_env().auto_send();
    let handler = Update::filter_message()
        .branch(
            dptree::entry()
                .filter_command::<Start>()
                .reply("**Hello!** __Send me a YouTube link!__"),
        )
        .branch(
            dptree::entry()
                .filter_command::<Download>()
                .perform_job(|ctx: UpdateWithCx<Message>, cmd: Download| async move {
                    let bot = ctx.bot().clone();
                    let tmp_dir = std::env::temp_dir();
                    let video_path = tmp_dir.join("video.mp4");

                    let output = Command::new("youtube-dl")
                        .arg("-f")
                        .arg(format!("bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"))
                        .arg("-o")
                        .arg(video_path.to_str().unwrap())
                        .arg(&cmd.link)
                        .output()?;

                    if output.status.success() {
                        ctx.reply_with_video(teloxide::types::InputFile::file(video_path), "**Video downloaded!**")
                            .await?;
                        fs::remove_file(video_path)?;
                    } else {
                        ctx.reply("**Error!** __Check console.__").await?;
                    }

                    Ok(())
                }),
        )
        .branch(
            dptree::entry()
                .filter_message()
                .condition(|msg: &Message| {
                    msg.text().map(|text| {
                        text.contains("https://www.youtube.com/") || text.contains("https://youtu.be/")
                    })
                    .unwrap_or(false)
                })
                .perform_job(|ctx: UpdateWithCx<Message>| async move {
                    let link = ctx.update.message().unwrap().text().unwrap().to_string();
                    let resolutions = vec!["720p", "480p", "360p", "240p", "144p"];
                    let markup = InlineKeyboardMarkup::new(
                        resolutions
                            .iter()
                            .map(|res| {
                                InlineKeyboardButton::callback(
                                    format!("{} {}", get_random_emoji(), res),
                                    res.to_string(),
                                )
                            })
                            .collect(),
                    );
                    ctx.reply("Pick a resolution:", markup).await?;
                    ctx.input_handle().command(Download { link, resolution: "".to_string() }).await
                }),
        );

    Dispatcher::builder(bot, handler)
        .dependencies(dptree::deps![])
        .build()
        .dispatch()
        .await;

    Ok(())
}

fn get_random_emoji() -> &'static str {
    let emojis = ["🔥", "🍬", "🌹", "🎂", "👀", "😜", "🎶"];
    emojis[rand::random::<usize>() % emojis.len()]
}
