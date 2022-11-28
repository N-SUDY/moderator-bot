## About
This bot is designed to simplify the moderation and management of Telegram groups.

<p align="center">
    <img src="https://img.shields.io/badge/license-GPL-blue">
</p>

## Features

* Ban,mute users(for a specified time) 
* Member roles       
* Report users
* User complaints
* Save admin actions in database

## Installation

- Required:Python3 3.x,poetry/pip.
- Clone this repo.
- Telegram API Service on port 5326.
- Move the .env.dist text template to .env and configure him.
- First start use `!reload` for parsing members and permissions

## Configuration .env

| environment variables             | description                      |
|-----------------------------------|----------------------------------|
| `bot_token`                       | Telegram bot token               |
| `telegram_bot_api_server`         | Telegram bot api server          |
| `db_url`                          | Connection info to database      |
| `api_id` and `api_hash`           | Telegram application data        |
| `group_id`                        | Group id                         |
| `second_group_id`                 | Seconds group for admins         |
| `vt_api`                          | VirusTotalAPI token (optionaly)  |

## TODO  

- [ ] Docker
- [ ] Systemd unit
- [ ] Antiflood system                          
- [ ] Silent commands
- [ ] Site for group moderator

## Support 
Every investition helps in maintaining this project and making it better.

<img src="https://img.shields.io/badge/btc-bc1qzp7q3rghzcx70534e7xf6tj0ns3dqvvnex80kf-green?logo=bitcoin">
