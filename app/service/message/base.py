from aio_pika import connect, Message


class MessageBroker:
    def __init__(self, connection_parameters, name_queue):
        self.connection = None
        self.channel = None
        self.listener_queue = None
        self.name_queue = name_queue
        self.exchange = None
        self.connection_parameters = connection_parameters

    async def connect_to_rabbitmq(self):
        self.connection = await connect(self.connection_parameters)

    async def create_channel(self):
        self.channel = await self.connection.channel()

    async def declare_queue_and_exchange(self):
        self.listener_queue = await self.channel.declare_queue(self.name_queue)
        self.exchange = await self.channel.declare_exchange("my_exchange", type="direct")
        await self.listener_queue.bind(self.exchange, "my_routing_key")

    async def publish_message(self, message_body):
        message = Message(message_body.encode())
        await self.exchange.publish(message, routing_key="my_routing_key")

    async def consume_messages(self):
        async with self.listener_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print("Mensagem recebida:", message.body.decode())
