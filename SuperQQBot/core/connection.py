from typing import overload
from json import dumps

import requests
from requests import post, get, JSONDecodeError
from .Error import *

Authorization_TYPES = "QQBot"


def get_authorization(access_token) -> str:
    return f"{Authorization_TYPES} {access_token}"
def my_ipaddress() -> str:
    try:
        response = get("https://searchplugin.csdn.net/api/v1/ip/get").json()
        return response["data"]["ip"]
    except :
        return "未知"

class BaseConnect:
    def __init__(self, function: str, access_token: str, url: str | bool = False):
        self.response = None
        if not isinstance(url, str):
            url = "https://sandbox.api.sgroup.qq.com" \
                if url else "https://api.sgroup.qq.com/"
        self.url = url + function
        self.access_token = access_token
    def is_error(self) -> bool:
        return self.response.status_code != 200 or "err_code" in self.response.json()

    def error_reason(self) -> str | None:
        if self.is_error():
            return self.response.json()["message"]
        else:
            return None

    def error_code(self) -> int | None:
        if self.is_error():
            return self.response.json()["code"]
        else:
            return None

    def verify_data(self) -> None:
        if self.error_code() is None:
            return
        elif self.error_code() == 11298:
            raise (
                IPNotInWhiteList(my_ipaddress()))
        elif self.error_code() == 100007 and self.error_reason() == 'appid invalid':
            return
        else:
            raise (
                UnknownError(self.response))

    def json(self) -> dict | None:
        self.verify_data()
        try:
            return self.response.json()
        except JSONDecodeError:
            return None

class PostConnect(BaseConnect):
    @overload
    def __init__(self, function: str, json: dict, access_token: str, url: bool = False):
        pass

    @overload
    def __init__(self, function: str, json: dict, access_token: str, url: str = "https://api.sgroup.qq.com/"):
        pass

    @overload
    def __init__(self, function: str, json: str, access_token: str, url: str = "https://api.sgroup.qq.com/"):
        pass

    @overload
    def __init__(self, function: str, json: str, access_token: str, url: bool = False):
        pass

    def __init__(self, function: str, json, access_token: str, url: str | bool = False):
        super().__init__(function=function, url=url, access_token=access_token)
        if isinstance(json, dict):
            payload = dumps(json)
        elif isinstance(json, str):
            payload = json
        else:
            raise ValueError("给的什么玩意儿啊这是，这还是合法Json吗？")
        self.response = post(url=self.url,
                             headers={'Content-Type': 'application/json',
                                      'Authorization': get_authorization(self.access_token)},
                             data=payload)
        self.text = self.response.text




class GetConnect(BaseConnect):
    @overload
    def __init__(self, function: str, access_token: str, url: bool = False):
        pass

    @overload
    def __init__(self, function: str, access_token: str, url: str = "https://api.sgroup.qq.com/"):
        pass

    @overload
    def __init__(self, function: str, access_token: str, url: str = "https://api.sgroup.qq.com/"):
        pass

    @overload
    def __init__(self, function: str, access_token: str, url: bool = False):
        pass

    def __init__(self, function: str, access_token: str, url: str | bool = False):
        super().__init__(url=url, function=function, access_token=access_token)
        self.response = get(url=self.url,
                            headers={'Content-Type': 'application/json',
                                     'Authorization': get_authorization(self.access_token)})
        self.text = self.response.text



