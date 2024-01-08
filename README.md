# Tinkoff Invest Bot
Telegram bot that uses https://www.tinkoff.ru/invest to find most profitable bonds in different ratings.
## Usage
1. Create .env file like example.env and fill in tokens.
2. 
   - If you have **Make** tool installed, run `make -j2` command.
   - If not, run commands:
     ```
     docker-compose up -d
     python rpc/rpc_server.py
     python bot.py
     ```
3. Open your Telegram Bot and use commands:
    ```
   /start
   /high
   /medium
   /all
    ```
## Used technologies
1. TelegramAPI
2. TinkoffAPI
3. Docker
4. RabbitMQ
