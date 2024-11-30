import datetime
from json import dumps
from typing import Optional

from requests import post, get, JSONDecodeError, delete, put

from .Error import *

Authorization_TYPES = "QQBot"


def get_authorization(access_token) -> str:
    return f"{Authorization_TYPES} {access_token}"


def my_ipaddress() -> str:
    try:
        response = get("https://searchplugin.csdn.net/api/v1/ip/get").json()
        return response["data"]["ip"]
    except:
        return "未知"


class BaseConnect:
    def __init__(self, function: str, access_token: str, url: str | bool = False):
        self.response = None
        if not isinstance(url, str):
            url = "https://sandbox.api.sgroup.qq.com" \
                if url else "https://api.sgroup.qq.com/"
        self.url = (url if not url.endswith("/") else url[:-1]) + function
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
                UnknownError(
                    f"\nt={self.response.text};c={self.response};r={self.response.request.body};u={self.response.request.url};m={self.response.request.method};r={self.response.reason}"))

    def json(self) -> dict | None:
        self.verify_data()
        try:
            json_result = self.response.json()
            if isinstance(json_result, list):
                for i in json_result:
                    if "timestamp" in i.keys():
                        i["timestamp"] = datetime.datetime.fromisoformat(i["timestamp"])
            else:
                if "timestamp" in json_result.keys():
                    json_result["timestamp"] = datetime.datetime.fromisoformat(json_result["timestamp"])
            return json_result
        except JSONDecodeError:
            return None


class PostConnect(BaseConnect):

    def __init__(self, function: str, access_token: str, json: dict | str, url: str | bool = False):
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
    def __init__(self, function: str, access_token: str, url: str | bool = False, query: Optional[dict] = None):
        super().__init__(url=url, function=function, access_token=access_token)
        if query is not None:
            self.url += "?" + "&".join([f"{key}={value}" for key, value in query.items()])
        self.response = get(url=self.url,
                            headers={'Content-Type': 'application/json',
                                     'Authorization': get_authorization(self.access_token)})
        self.text = self.response.text


class DeleteRequests(BaseConnect):
    def __init__(self, function: str, access_token: str, url: str | bool = False, headers: Optional[dict] = None):
        super().__init__(url=url, function=function, access_token=access_token)
        self.response = delete(url=self.url,
                               headers={'Content-Type': 'application/json',
                                        'Authorization': get_authorization(self.access_token),
                                        **headers})
        self.text = self.response.text


class PutRequests(BaseConnect):
    def __init__(self, function: str, access_token: str, url: str | bool = False):
        super().__init__(url=url, function=function, access_token=access_token)
        self.response = put(url=self.url,
                            headers={'Content-Type': 'application/json',
                                     'Authorization': get_authorization(self.access_token)})
        self.text = self.response.text
