use std::fs;
use std::path::Path;

pub struct Config {
    pub bot_token: String,
}

impl Config {
    pub fn load_config() -> Result<Self, std::io::Error> {
        let contents = fs::read_to_string("config.txt")?;
        let bot_token = contents.trim().to_string();
        Ok(Config { bot_token })
    }
}
