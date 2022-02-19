from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Callable, Dict, List, Optional, Union
from inspect import _empty, signature
import os
import json


class TraqBot:
    """Create a new traQ bot that provides functionalities to register event handler.

    import os
    from traq_bot import TraqBot

    # Initializes your bot with your bot token
    bot = TraqBot(verification_token=os.environ.get("BOT_VERIFICATION_TOKEN"))

    # Register event handler
    @bot.message_created
    def message_created(data):
        print(data)

    # Start your app
    if __name__ == "__main__":  
        bot.run()  

    Args:
        verificaiton_token (str): Your bot token.
    """

    def __init__(self, verification_token: Optional[str]):
        self._verification_token: Optional[str] = verification_token or os.environ.get(
            "BOT_VERIFICATION_TOKEN", None
        )

        self._handlers: Dict[str, List[Callable[[Optional[Dict]], None]]] = {
            "PING": [],
            "JOINED": [],
            "LEFT": [],
            "MESSAGE_CREATED": [],
            "MESSAGE_DELETED": [],
            "MESSAGE_UPDATED": [],
            "DIRECT_MESSAGE_CREATED": [],
            "DIRECT_MESSAGE_DELETED": [],
            "DIRECT_MESSAGE_UPDATED": [],
            "BOT_MESSAGE_STAMPS_UPDATED": [],
            "CHANNEL_CREATED": [],
            "CHANNEL_TOPIC_CHANGED": [],
            "USER_CREATED": [],
            "STAMP_CREATED": [],
            "TAG_ADDED": [],
            "TAG_REMOVED": []
        }

    def run(self, port: int = 8080) -> None:
        """Start your bot.

        Args:
            port (int): Port number. Defaults to 8080.
        """
        self._bot_server: TraqBotServer = TraqBotServer(port=port, bot=self)
        self._bot_server.run()

    def _handle_event(self, event: str, data: Dict) -> Dict:
        if event == "PING":
            # 204返す
            resp = {
                "status": 204,
                "headers": {},
                "body": ""
            }
            return resp

        if len(self._handlers[event]) == 0:
            resp = {
                "status": 501,
                "headers": {},
                "body": ""
            }
            return resp

        try:
            # 各イベントに対するハンドラを実行
            for func in self._handlers[event]:
                sig = signature(func)
                # 引数をを持たなければそのまま関数を実行する
                if len(sig.parameters) == 0:
                    func()
                # もし引数を1つ持っていたら`data`を与えて関数を実行する
                elif ((len(sig.parameters) == 1) and (next(iter(sig.parameters.values())).annotation in [Dict, _empty])):
                    func(data)
                else:
                    raise Exception("イベントハンドラは0または1つの辞書型の引数を取るようにしてください")
            # ここで204返す
            resp = {
                "status": 204,
                "headers": {},
                "body": ""
            }
            return resp
        except Exception as e:
            print(e)
            # ここで500とか返す
            resp = {
                "status": 500,
                "headers": {},
                "body": ""
            }
            return resp

    def _register_function(self, func: Callable[[Optional[Dict]], None], event: str) -> None:
        self._handlers[event].append(func)

    def ping(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register ping event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        """
        self._register_function(func, "PING")
        return func

    def joined(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register joined event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "JOINED")
        return func

    def left(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register left event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "LEFT")
        return func

    def message_created(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register message created event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "MESSAGE_CREATED")
        return func

    def message_deleted(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register joined message deleted handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "MESSAGE_DELETED")
        return func

    def message_updated(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register message updated event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "MESSAGE_UPDATED")
        return func

    def direct_message_created(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register direct message created event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "DIRECT_MESSAGE_CREATED")
        return func

    def direct_message_deleted(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register direct message deleted event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "DIRECT_MESSAGE_DELETED")
        return func

    def direct_message_updated(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register direct message updated event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "DIRECT_MESSAGE_UPDATED")
        return func

    def bot_message_stamps_updated(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register bot message stamps updated event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "BOT_MESSAGE_STAMPS_UPDATED")
        return func

    def channel_created(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register channel created event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "CHANNEL_CREATED")
        return func

    def channel_topic_changed(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register channel topic changed event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "CHANNEL_TOPIC_CHANGED")
        return func

    def user_created(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register user created event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "USER_CREATED")
        return func

    def stamp_created(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register stamp created event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "STAMP_CREATED")
        return func

    def tag_added(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register tag added event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "TAG_ADDED")
        return func

    def tag_removed(self, func: Callable[[Optional[Dict]], None]) -> Callable[[Optional[Dict]], None]:
        """Register tag removed event handler. This method can be used as either a decorator or a method.

        Args:
            func (Callable[[Optional[Dict]], None]): Function to be registered. This function can take zero or one argument. If it takes an argument, it will execute the handler by giving the body received when the event is received as an argument.
        Returns:
            Callable[[Optional[Dict]], None]
        """
        self._register_function(func, "TAG_REMOVED")
        return func


class TraqBotServer:
    def __init__(self, port: int, bot: TraqBot):
        self._port: int = port
        self._bot: TraqBot = bot
        _bot: TraqBot = self._bot

        class TraqBotHandler(SimpleHTTPRequestHandler):
            def do_POST(self) -> None:
                content_length: int = int(
                    self.headers.get('Content-Length')) or 0

                verification_token: Optional[str] = self.headers.get(
                    'X-TRAQ-BOT-TOKEN'
                )
                if verification_token is None:
                    print("No X-TRAQ-BOT-TOKEN")
                    self._send_response(401, {}, "")
                    return
 
                if verification_token != _bot._verification_token:
                    print("Verification token mismatch")
                    self._send_response(401, {}, "")
                    return

                event: Optional[str] = self.headers.get("X-TRAQ-BOT-EVENT")
                if event is None:
                    print("No X-TRAQ-BOT-EVENT")
                    self._send_response(400, {}, "")
                    return

                request_body: bytes = self.rfile.read(content_length)
                if len(request_body) == 0:
                    data: Dict = {}
                else:
                    try:
                        data: Dict = json.loads(request_body.decode('utf-8'))
                    except json.JSONDecodeError:
                        print("JSONDecodeError")
                        self._send_response(400, {}, "")
                        return

                bot_resp = _bot._handle_event(event, data)
                self._send_bot_response(bot_resp)

            def _send_response(self, status: int, headers: Dict, body: Union[str, Dict]) -> None:
                self.send_response(status)

                response_body = body if isinstance(
                    body, str) else json.dumps(body)
                response_body.encode('utf-8')
                byte_body = response_body.encode('utf-8')

                for k, vs in headers.items():
                    for v in vs:
                        self.send_header(k, v)
                self.send_header('Content-Length', len(byte_body))
                self.end_headers()
                self.wfile.write(byte_body)

            def _send_bot_response(self, bot_resp: Dict) -> None:
                self._send_response(
                    status=bot_resp["status"],
                    headers=bot_resp["headers"],
                    body=bot_resp["body"]
                )

        self._server: HTTPServer = HTTPServer(
            ("0.0.0.0", self._port), TraqBotHandler)

    def run(self) -> None:
        try:
            print("serving at port", self._port)
            self._server.serve_forever(0.05)
        finally:
            self._server.server_close()
