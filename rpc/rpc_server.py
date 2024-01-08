import asyncio

from aio_pika import connect_robust
from aio_pika.patterns import RPC

from tinkoff_bonds.bonds import async_best_bonds_message


async def main() -> None:
    connection = await connect_robust(
        "amqp://guest:guest@localhost/",
        client_properties={"connection_name": "callee"},
    )

    # Creating channel
    channel = await connection.channel()

    rpc = await RPC.create(channel)
    await rpc.register('get_bonds_message', async_best_bonds_message, auto_delete=True)

    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
