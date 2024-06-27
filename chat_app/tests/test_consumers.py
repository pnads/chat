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

    async def test_invalid_message_format(self):
        communicator = WebsocketCommunicator(application, "/ws/chat/testroom/")
        await communicator.connect()

        # Send invalid message format
        await communicator.send_json_to({"invalid_key": "This should not work"})

        # Test receiving the error message
        response = await communicator.receive_json_from()
        self.assertEqual(response, {"error": "Invalid message format"})

        await communicator.disconnect()

    async def test_different_rooms(self):
        communicator1 = WebsocketCommunicator(application, "/ws/chat/room1/")
        communicator2 = WebsocketCommunicator(application, "/ws/chat/room2/")
        await communicator1.connect()
        await communicator2.connect()

        # Send message from communicator1
        await communicator1.send_json_to({"message": "Message from room1"})

        # Test that communicator2 does not receive the message
        with self.assertRaises(Exception):
            await communicator2.receive_json_from()

        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_broadcast_to_correct_room(self):
        communicator1 = WebsocketCommunicator(application, "/ws/chat/room1/")
        communicator2 = WebsocketCommunicator(application, "/ws/chat/room1/")
        communicator3 = WebsocketCommunicator(application, "/ws/chat/room2/")
        await communicator1.connect()
        await communicator2.connect()
        await communicator3.connect()

        # Send message from communicator1 to room1
        await communicator1.send_json_to({"message": "Hello room1"})

        # Test that communicator2 receives the message
        response = await communicator2.receive_json_from()
        self.assertEqual(response, {"message": "Hello room1"})

        # Test that communicator3 does not receive the message
        with self.assertRaises(Exception):
            await communicator3.receive_json_from()

        await communicator1.disconnect()
        await communicator2.disconnect()
        await communicator3.disconnect()
