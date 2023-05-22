import pika


class Consumer:

    def __init__(
        self, 
        host: 'str',
        port: 'int', 
        queue: 'str', 
        callback
    ):
        self._parameters = pika.ConnectionParameters(
            host=host, 
            port=port
        )

        self._connection = pika.BlockingConnection(self._parameters)

        self._channel = self._connection.channel()
        self._queue = queue
        self._callback = callback

    def _subscribe(self):
        self._channel.queue_declare(
            queue=self._queue, 
            exclusive=True, 
            auto_delete=True
        )
        
        self._channel.basic_consume(
            queue=self._queue,
            on_message_callback=self._callback
        )

    def start(self):
        self._subscribe()
        self._channel.start_consuming()

    def close(self):
        self._channel.close()
