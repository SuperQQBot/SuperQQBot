class IPNotInWhiteList(Exception):
    def __init__(self, ipaddress:str):
        self.ipaddress = ipaddress
    def __str__(self):
        return (f"您的IP不在白名单内，您的IP是{self.ipaddress}，"
                "请前往https://q.qq.com/qqbot/#/developer/developer-setting添加IP白名单")
class UnknownAppId(Exception):
    def __init__(self, set_appId):
        super().__init__(set_appId)
        self.set_appId = set_appId
    def __str__(self):
        return ("您配置的AppId无效，"
                "请前往https://q.qq.com/qqbot/#/developer/developer-setting获取正确的App ID"
                "如果您确认获取了正确的App ID，"
                f"请尝试访问https://q.qq.com/qqbot/#/home?appid={self.set_appId}，"
                "如果可以访问到您的机器人界面，请向开发者反馈")
class UnknownAccessToken(Exception):
    def __str__(self):
        return "未知的AccessToken"


class UnknownError(Exception):
    def __init__(self, response):
        super().__init__(response)
        self.response = response

    def __str__(self):
        return ("未知错误，请联系开发者\n"
                "如果联系开发者，请提供以下信息"
                f"Server_response : {self.response}")
class AppIdAndSecretDoNotMatch(Exception):
    def __str__(self):
        return ("您配置的AppId与Secret不匹配，"
                "请前往https://q.qq.com/qqbot/#/developer/developer-setting"
                "获取正确的AppID（机器人ID）和AppSecret（机器人密钥）"
                "如果您确认获取了正确的AppID和Secret，"
                "请向开发者反馈")

class InvalidIntentsError(Exception):
    def __init__(self, response):
        super().__init__(response)
        self.response = response

    def __str__(self):
        return ("无效的意图配置，请检查您的intents设置\n"
                f"Server_response : {self.response}")
