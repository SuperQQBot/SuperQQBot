from .client import Intents
from .. import Token


class Client:
    def __init__(self, intents: Intents):
        self.access_token = None
        self.intents = intents

    def run(self, appId, clientSecret):
        self.token_class = Token(appId=appId, client_secret=clientSecret)
