run: start_docker start_rpc_server start_botq
start_docker:
        docker-compose up -d
start_rpc_server:
        python rpc/rpc_server.py
start_bot:
        python bot.py
