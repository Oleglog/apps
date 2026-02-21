import unittest
import socketio
import requests
import threading
import time

SERVER_URL = "http://localhost:3000"


class ChatAppTest(unittest.TestCase):

    def setUp(self):
        self.sio1 = socketio.Client()
        self.sio2 = socketio.Client()

    def tearDown(self):
        if self.sio1.connected:
            self.sio1.disconnect()
        if self.sio2.connected:
            self.sio2.disconnect()

    # 1. HTTP сервер работает
    def test_http_server_running(self):
        response = requests.get(SERVER_URL)
        self.assertEqual(response.status_code, 200)

    # 2. Socket подключается
    def test_socket_connection(self):
        self.sio1.connect(SERVER_URL)
        self.assertTrue(self.sio1.connected)

    # 3. Новый пользователь получает приветствие
    def test_user_join_message(self):
        event = threading.Event()
        result = {"found": False}

        @self.sio1.on("chat message")
        def on_message(data):
            if "Добро пожаловать" in data.get("text", ""):
                result["found"] = True
                event.set()

        self.sio1.connect(SERVER_URL)

        event.wait(timeout=3)

        self.assertTrue(result["found"])

    # 4. Сообщение отправляется и принимается
    def test_message_broadcast(self):
        event = threading.Event()

        @self.sio1.on("chat message")
        def on_message(data):
            if data.get("text") == "Привет":
                event.set()

        self.sio1.connect(SERVER_URL)
        time.sleep(0.5)

        self.sio1.emit("chat message", "Привет")

        event.wait(timeout=3)
        self.assertTrue(event.is_set())

    # 5. Сообщение получает второй клиент
    def test_multiple_clients_receive_message(self):
        event = threading.Event()

        @self.sio2.on("chat message")
        def on_message(data):
            if data.get("text") == "Общее":
                event.set()

        self.sio1.connect(SERVER_URL)
        self.sio2.connect(SERVER_URL)
        time.sleep(0.5)

        self.sio1.emit("chat message", "Общее")

        event.wait(timeout=3)
        self.assertTrue(event.is_set())

    # 6. Проверка отключения
    def test_disconnect(self):
        self.sio1.connect(SERVER_URL)
        self.sio1.disconnect()
        self.assertFalse(self.sio1.connected)


if __name__ == "__main__":
    unittest.main()