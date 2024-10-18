import importlib
import os


i = None

class NoModDirHasBeenCreate(Exception):
    def __init__(self):
        os.mkdir("mods")
    def __str__(self):
        return "找不到模组目录，请在创建的mod文件夹中放入外设mod"
def load_mod(mod_name:str):
    global i
    if mod_name.endswith(".py"):
        mod_name = mod_name[:-3]
    if "mods" not in os.listdir():
        raise (
            NoModDirHasBeenCreate)
    elif mod_name + ".py" not in os.listdir("mods"):
        raise (
            ImportError("未找到该模组"))
    elif "mod_loader.py" not in os.listdir("mods"):
        raise (
            ImportError("外设加载器未启用，请转载mod_loader"))
    else:
        importlib.import_module("mods.mod_loader")
    replace = importlib.import_module(f"mods.{mod_name}")
    for i in replace.Replace.keys():
        i = replace.Replace[i]