# SuperQQBot/ext/loader.py
import importlib
import os
import warnings
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
            # 由于 loader.py 不在 core 目录下，需要正确指定路径
            mod = importlib.import_module(f'{self.mods_path.stem}.{mod_name}', package=self.mods_path.stem)
            if hasattr(mod, 'setup'):
                mod.setup()
                self.mods.append(mod_name)
            else:
                warnings.warn(f"找不到 setup 函数，无法加载模组 {mod_name}")
        except ImportError as e:
            warnings.warn(f"无法加载模组 {mod_name}: {e}")

