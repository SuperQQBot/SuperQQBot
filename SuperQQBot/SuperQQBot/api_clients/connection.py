from abc import ABC
from datetime import datetime
from json import dumps, JSONDecodeError
from typing import Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .exceptions import *

Authorization_TYPES = "QQBot"


def get_authorization(access_token) -> str:
    return f"{Authorization_TYPES} {access_token}"


def my_ipaddress() -> str:
    try:
        response = httpx.get("https://searchplugin.csdn.net/api/v1/ip/get").json()
        return response["data"]["ip"]
    except:
        return "未知"


class BaseConnect(ABC):
    def __init__(self, function: str, access_token: str, url: str | bool = False):
        self.response = None
        if not isinstance(url, str):
            url = "https://sandbox.api.sgroup.qq.com" if url else "https://api.sgroup.qq.com/"
        self.url = url.rstrip("/") + function
        self.access_token = access_token
        self.client = None

    async def create_client(self):
        if self.client is None:
            self.client = httpx.AsyncClient(
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=50),
                timeout=httpx.Timeout(10.0, connect=5.0, read=10.0)
            )
        return self.client

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
                UnknownException(
                    f"\nt={self.response.text};c={self.response};r={self.response.request.body};u={self.response.request.url};m={self.response.request.method};r={self.response.reason}"))

    def json(self) -> dict | None:
        self.verify_data()
        try:
            json_result = self.response.json()
            if isinstance(json_result, list):
                for i in json_result:
                    if "timestamp" in i.keys():
                        i["timestamp"] = datetime.fromisoformat(i["timestamp"])
            else:
                if "timestamp" in json_result.keys():
                    json_result["timestamp"] = datetime.fromisoformat(json_result["timestamp"])
            return json_result
        except JSONDecodeError:
            return None

    async def apply(self):
        raise NotImplementedError("子类必须实现 apply() 方法")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
    async def apply_with_retry(self):
        return await self.apply()


class PostConnect(BaseConnect):
    def __init__(self, function: str, access_token: str, json: dict | str, url: str | bool = False):
        super().__init__(function, access_token, url)
        self.response = None
        self.text = None
        self.json = json

    async def apply(self):
        client = await self.create_client()
        try:
            if isinstance(self.json, dict):
                payload = dumps(self.json)
            elif isinstance(self.json, str):
                payload = self.json
            else:
                raise ValueError("Invalid JSON payload")

            self.response = await client.post(
                self.url,
                headers={'Content-Type': 'application/json', 'Authorization': get_authorization(self.access_token)},
                content=payload,
                timeout=10.0
            )
            self.text = self.response.text
            return self
        except httpx.RequestError as e:
            raise NetworkError(f"HTTP 请求失败: {str(e)}") from e


class GetConnect(BaseConnect):
    def __init__(self, function: str, access_token: str, url: str | bool = False, query: Optional[dict] = None):
        super().__init__(function, access_token, url)
        self.query = query

    async def apply(self):
        client = await self.create_client()
        try:
            self.response = await client.get(
                self.url,
                headers={'Content-Type': 'application/json', 'Authorization': get_authorization(self.access_token)},
                params=self.query,
                timeout=10.0  # 设置超时
            )
            self.text = self.response.text
            return self
        except httpx.RequestError as e:
            raise NetworkError(f"HTTP 请求失败: {str(e)}") from e


# connection.py - 修改 DeleteRequests 类
class DeleteRequests(BaseConnect):
    def __init__(self,
                 function: str,
                 access_token: str,
                 url: str | bool = False,
                 headers: Optional[dict] = None,
                 json_data: Optional[dict] = None):  # 新增 json_data 参数
        super().__init__(function, access_token, url)
        self.headers = headers
        self.json_data = json_data  # 存储 JSON 数据
        self.response = None
        self.text = None

    async def apply(self):
        client = await self.create_client()
        try:
            self.response = await client.delete(
                self.url,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': get_authorization(self.access_token),
                    **(self.headers or {})
                },
                params=self.json_data,  # 添加 json 参数
                timeout=10.0
            )
            self.text = self.response.text
            return self
        except httpx.RequestError as e:
            raise NetworkError(f"HTTP 请求失败: {str(e)}") from e


class PutRequests(BaseConnect):
    def __init__(self, function: str, access_token: str, url: str | bool = False):
        super().__init__(function, access_token, url)
        self.response = None
        self.text = None

    async def apply(self):
        client = await self.create_client()
        try:
            self.response = await client.put(
                self.url,
                headers={'Content-Type': 'application/json', 'Authorization': get_authorization(self.access_token)},
                timeout=10.0
            )
            self.text = self.response.text
            return self
        except httpx.RequestError as e:
            raise NetworkError(f"HTTP 请求失败: {str(e)}") from e
