from aio_pika import connect_robust
from aio_pika.patterns import RPC


async def get_rpc_client():
    connection = await connect_robust(
        "amqp://guest:guest@localhost/",
        client_properties={"connection_name": "caller"},
    )

    async with connection:
        # Creating channel
        channel = await connection.channel()

        rpc = await RPC.create(channel)
        while True:
            yield rpc
