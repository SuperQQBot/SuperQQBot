# core_loader.py
import importlib
import warnings
from pathlib import Path

from .Error import UnAuthenticated, UsingBetaFunction, UsingCompatibilityMode
from .log import get_logger

# 定义支持的模组类型
SUPPORTED_MOD_TYPES = {"test", "trans_old", "other"}

logger = get_logger()
def _initialize():
    pass
_is_authenticated = False

def _check_authentication():
    if not _is_authenticated:
        raise UnAuthenticated

def authenticate(mod_type:str):
    _initialize()
    if mod_type == "mod_loader":
        warnings.warn(f"模组类型 {mod_type} 不在支持的类型中，请使用支持的类型")
        return
    global _is_authenticated
    _is_authenticated = True
    logger.info("模组加载器认证成功，允许使用模块")


class CoreModLoader:
    def __init__(self, base_path="mods"):
        _check_authentication()
        self.base_path = base_path
        self.mods = []

    def find_mods(self):
        """查找所有可用的模组"""
        for item in Path(self.base_path).iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                yield item.name
            elif item.is_file() and item.suffix == ".py":
                yield item.name

    def load_mod(self, mod_name):
        try:
            mod = importlib.import_module(f"{self.base_path}.{mod_name}", package=self.base_path)
            if hasattr(mod, 'setup'):
                if hasattr(mod, 'TYPES'):
                    if mod.TYPES not in SUPPORTED_MOD_TYPES:
                        warnings.warn(f"模组 {mod_name} 的 TYPES 类型不正确，请使用支持的类型")
                        return
                    else:
                        if mod.TYPES == "test":
                            warnings.warn(UsingBetaFunction("test"))
                        elif mod.TYPES == "trans_old":
                            warnings.warn(UsingCompatibilityMode())
                        elif mod.TYPES == "other":
                            warnings.warn("你正在使用的模组未指定其类型，可能无法提供对应的支持")
                        mod.setup()
                    self.mods.append(mod_name)
                else:
                    warnings.warn(f"模组 {mod_name} 未定义 TYPES（他的类型），无法加载")
            else:
                warnings.warn(f"找不到 setup 函数，无法加载模组 {mod_name}")
        except ImportError as e:
            warnings.warn(f"无法加载模组 {mod_name}: {e}")
    def load_all_mods(self):
        for mod_name in self.find_mods():
            self.load_mod(mod_name)