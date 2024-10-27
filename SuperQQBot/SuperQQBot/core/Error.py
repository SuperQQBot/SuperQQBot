class IPNotInWhiteList(Exception):
    def __init__(self, ipaddress: str):
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
        return ("未知错误，请联系开发者（邮箱：trustedinster@outlook.com或通过Issues提交）\n"
                "如果联系开发者，请提供以下信息："
                f"{self.response}")


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


class ExecutionSequenceError(Exception):
    def __init__(self, should_do_first, but_user_do_first):
        super().__init__(should_do_first, but_user_do_first)
        self.do_first = should_do_first
        self.do_secondly = but_user_do_first

    def __str__(self):
        return f"执行顺序有误，应当先执行{self.do_first}然后再执行{self.do_secondly}，但事实上是先执行了{self.do_secondly}"


class CompatibilityWillBeUnSuppose(Warning):
    def __init__(self, old_version, new_version):
        super().__init__(old_version, new_version)
        self.old_version = old_version
        self.new_version = new_version

    def __str__(self):
        return f"平替拓展支持模块提醒：你正在使用可能被放弃支持QQBotPy方法，为了保证您程序的稳定性，请将{self.old_version}替换为{self.new_version}"


class UsingCompatibilityMode(Warning):
    def __str__(self):
        return "虽然兼容性设置可以解决大部分问题，但不代表兼容性设置是可被接受的。由于技术原因，部分兼容性设置可能导致无法正常运行"


class UnknownKwargs(Exception):
    def __init__(self, kwarg_name, should_in, but_give):
        super().__init__(kwarg_name, should_in, but_give)
        self.kwarg_name = kwarg_name
        self.should_in = should_in
        self.but_give = but_give

    def __str__(self):
        return f"未知的{self.kwarg_name}，应该在{self.should_in}，但是给予了我们{self.but_give}"


class UnSupposeUsage(Exception):
    def __init__(self, un_suppose_usage):
        super().__init__(un_suppose_usage)
        self.un_suppose_usage = un_suppose_usage

    def __str__(self):
        return f"{self.un_suppose_usage}已不再受支持"


class WrongArgs(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return {self.message}


class ParameterMappingFailed(Exception):
    def __init__(self, parameter1, parameter2, value1, value2):
        super().__init__(parameter1, parameter2, value1, value2)
        self.value2 = value2
        self.value1 = value1
        self.parameter2 = parameter2
        self.parameter1 = parameter1

    def __str__(self):
        return f"不能在{self.parameter1}={self.value1}时让{self.parameter2}={self.value2}"

class UsingBetaFunction(Warning):
    def __init__(self, beta_function_name):
        super().__init__(beta_function_name)
        self.beta_function_name = beta_function_name
    def __str__(self):
        return f"正在使用Beta功能：{self.beta_function_name}，这意味着此功能可能存在Bug，因此产生的事故或消息错误作者无法承担"
