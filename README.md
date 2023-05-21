## About
This bot is designed to simplify the moderation and management of Telegram groups.

## Features

* User roles
* User complains system
* Admin activity log

## Up

- Required: python3.11
- Up Telegram Bot API server on port 5326
- Use the .env.dist template example for creating .env 
- After first start use `!reload` for parsing members list and permissions 

## Configuration .env

| environment variables         | description                      |
|-------------------------------|----------------------------------|
| `bot_token`                   | telegram bot token               |
| `api_id` and `api_hash`       | telegram application data        |
| `group_id`                    | group id                         |
| `second_group_id`             | seconds group for admins         |
| `telegram_bot_api_server`     | telegram bot api server          |
| `db_url`                      | connection info to database      |
| `limit_of_warns`              | limit user warnings              |
| `update_interval`             | interval for update of user data |    

## TODO  

- [ ] Multigroup support
- [ ] Integrate project with docker 
- [ ] Flood detection
- [ ] Web(in development)

## Support 

Every investition helps in maintaining this project and making it better.

<img src="https://img.shields.io/badge/btc-bc1qzp7q3rghzcx70534e7xf6tj0ns3dqvvnex80kf-green?logo=bitcoin">

Don't donate to this wallet yet, I've lost access to it. Wait until I restore the wallet or create a new one.
