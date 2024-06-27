from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from chat_project.asgi import application


class ChatConsumerTest(TransactionTestCase):
    async def test_websocket_connection(self):
        communicator = WebsocketCommunicator(application, "/ws/chat/testroom/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Test sending a message
        await communicator.send_json_to(
            {
                "message": "Hello, World!",
            }
        )

        # Test receiving the message
        response = await communicator.receive_json_from()
        self.assertEqual(
            response,
            {
                "message": "Hello, World!",
            },
        )

        # Test disconnecting
        await communicator.disconnect()

    async def test_message_broadcasting(self):
        communicator1 = WebsocketCommunicator(application, "/ws/chat/testroom/")
        communicator2 = WebsocketCommunicator(application, "/ws/chat/testroom/")
        await communicator1.connect()
        await communicator2.connect()

        # Send message from communicator1
        await communicator1.send_json_to(
            {
                "message": "Hello, everyone!",
            }
        )

        # Test if communicator2 receives the message
        response = await communicator2.receive_json_from()
        self.assertEqual(
            response,
            {
                "message": "Hello, everyone!",
            },
        )

        await communicator1.disconnect()
        await communicator2.disconnect()
