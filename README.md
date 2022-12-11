## About
This bot is designed to simplify the moderation and management of Telegram groups.

<p align="center">
    <img src="https://img.shields.io/badge/license-GPL-blue">
</p>

## Features

* Admin commands
* Member roles       
* Report users
* Silent commands
* User complaints
* Save admin actions in database

## Installation

- Required:python3.x, poetry/pip
- Clone this repo
- Telegram API Service on port 5326
- Move the .env.dist text template to .env and configure him
- First start use `!reload` for parsing members and permissions

## Configuration .env

| environment variables             | description                      |
|-----------------------------------|----------------------------------|
| `bot_token`                       | telegram bot token               |
| `telegram_bot_api_server`         | telegram bot api server          |
| `db_url`                          | connection info to database      |
| `api_id` and `api_hash`           | telegram application data        |
| `group_id`                        | group id                         |
| `second_group_id`                 | seconds group for admins         |

## TODO  

- [ ] Docker
- [ ] Systemd unit
- [ ] Write antithrotling midlware middleware(anti flood system)                         
- [ ] Site for group moderator(in development)

## Support 

Every investition helps in maintaining this project and making it better.

<img src="https://img.shields.io/badge/btc-bc1qzp7q3rghzcx70534e7xf6tj0ns3dqvvnex80kf-green?logo=bitcoin">
