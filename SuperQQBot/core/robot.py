from . import Error
from .connection import PostConnect
from . import log
from time import time

_log = log.get_logger()

class Token:
    def __init__(self, appId:str, client_secret:str):
        self.appId = appId
        self.client_secret = client_secret
        self.access_token = None
        self.active_time = None
        self.start = float()
        self.renew_access_token()

    def validate_accessToken(self) -> bool:
        return self.access_token is not None and self.active_time is not None
    def get_access_token(self) -> str:
        if not self.validate_accessToken():
            raise (
                Error.UnknownAccessToken)
        elif not self.is_access_token_activity():
            return self.renew_access_token()
        else:
            return self.access_token
    def is_access_token_activity(self) -> bool:
        return time() - self.start < self.active_time
    def renew_access_token(self):
        self.start = time() + 1
        response = PostConnect(function="/app/getAppAccessToken",
                               json={"appId": self.appId, "clientSecret": self.client_secret},
                               access_token="",
                               url="https://bots.qq.com")
        if response.is_error():
            if response.error_reason() == "internal err":
                raise (
                    Error.IPNotInWhiteList)
            elif response.error_code() == 100007:
                raise (
                    Error.UnknownAppId(self.appId))
            elif response.error_reason() == 'invalid appid or secret':
                raise (
                    Error.AppIdAndSecretDoNotMatch)
            else:
                raise (
                    Error.UnknownError(response.text))

        else:
            response = response.json()
            try:
                self.access_token = response["access_token"]
                self.active_time = int(response["expires_in"])
            except KeyError:
                raise (
                    Error.UnknownError(response))
            _log.info(f"[QQBot]AccessToken存活时间：{self.active_time}")
            return self.access_token