from time import time
from .connection import PostConnect, my_ipaddress
from . import exceptions
from ..logger.logger import WebHookLogger

logger = WebHookLogger()

# AccessToken类
class Token:
    def __init__(self, appId: str, client_secret: str):
        self.appId = appId
        self.client_secret = client_secret
        self.access_token = None
        self.active_time = None
        self.start = float()
        self.renew_access_token()

    def validate_access_token(self) -> bool:
        return self.access_token is not None and self.active_time is not None

    async def get_access_token(self) -> str:
        if not self.validate_access_token():
            raise exceptions.UnknownAccessToken()
        elif not self.is_access_token_activity():
            return await self.renew_access_token()
        else:
            return self.access_token

    def is_access_token_activity(self) -> bool:
        return time() - self.start < self.active_time

    async def renew_access_token(self):
        self.start = time()
        post_connect = PostConnect(
            url="https://bots.qq.com",
            function="/app/getAppAccessToken",
            access_token=self.access_token,
            json={"appId": self.appId, "clientSecret": self.client_secret}
        )  # 创建 PostConnect 实例并传递所有必要的参数
        await post_connect.apply()
        if post_connect.is_error():
            if post_connect.error_code() == 100007:
                raise exceptions.UnknownAppId(self.appId)
            elif post_connect.error_reason() == "internal err":
                raise exceptions.IPNotInWhiteList(ipaddress=await my_ipaddress())
            elif post_connect.error_reason() == 'invalid appid or secret':
                raise exceptions.AppIdAndSecretDoNotMatch()
            else:
                raise exceptions.UnknownException(post_connect.text)

        else:
            response = post_connect.json()
            try:
                self.access_token = response["access_token"]
                self.active_time = int(response["expires_in"])
            except KeyError:
                raise exceptions.UnknownException(response)
            logger.info(f"[QQBot]AccessToken存活时间：{self.active_time}")
            return self.access_token
