# SuperQQBot/ext/loader.py
import importlib
import os
import warnings
from SuperQQBot.core.Error import UsingBetaFunction, UsingCompatibilityMode
from pathlib import Path

if not os.getcwd().endswith("\\mods"):
    raise (
        ImportError("为了保证核心功能的安全，请使用mod_loader.py来进行导入"))


class ModLoader:
    def __init__(self):
        self.mods_path = Path("mods")
        self.mods = []

    def load_mod(self, mod_name):
        try:
            mod = importlib.import_module(f'{self.mods_path.stem}.{mod_name}', package=self.mods_path.stem)
            if hasattr(mod, 'setup'):
                if hasattr(mod, 'TYPES'):
                    if type(mod.TYPES) != str:
                        (warnings
                         .warn(f"模组 {mod_name} 的 TYPES 类型不正确，请使用字符串"))
                        return
                    if mod.TYPES.lower() == "test":
                        (warnings
                         .warn(UsingBetaFunction(mod_name)))
                    elif mod.TYPES.lower() == "trans_old":
                        (warnings
                         .warn(UsingCompatibilityMode()))
                    elif mod.TYPES.lower() == "other":
                        pass
                    else:
                        (warnings
                         .warn(f"模组 {mod_name} 的 TYPES 类型不正确，请使用 test/trans_old/other"))
                        return
                    mod.setup()
                    self.mods.append(mod_name)
                else:
                    (warnings
                     .warn(f"模组 {mod_name} 未定义 TYPES（他的类型），无法加载"))
            else:
                (warnings
                 .warn(f"找不到 setup 函数，无法加载模组 {mod_name}"))
        except ImportError as e:
            (warnings
             .warn(f"无法加载模组 {mod_name}: {e}"))

