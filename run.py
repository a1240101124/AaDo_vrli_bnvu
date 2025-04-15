r"""
创建者: 阿斗是只猫
创建日期: 2025-04-09
最后编辑人: 阿斗是只猫
最后编辑时间: 2025-04-13
说明:

    如有问题或建议，请联系微信公众号：【阿斗的小窝】

    Copyright (c) 2025 by 阿斗是只猫, All Rights Reserved.
"""

# 导入常用模块
from enum import Enum
from pathlib import Path
from turtle import width

from nicegui import app, native, ui

from 读写M import 配置C
from 配置M import (
    常量_一级_位置,
    常量_三极_位置,
    常量_二级_位置,
    常量_后缀,
    常量_后缀_最大,
    常量_四级_位置,
    常量_标题,
    常量_第一位,
    常量_第三位,
    常量_第二位,
    常量_第四位,
    常量_路径,
    常量_连接符,
)

####################################配置参数#############################################
图标路径G = 常量_路径 / Path("static/app_icon.ico")
项目路径G = 常量_路径.parent

第一位_索引G: int = 0  # 默认从索引0开始，即第一位的初始值为：1
第二位_索引G: int = 1  # 第二位的初始值默认为：0
第三位_索引G: int = 1  # 第三位的初始值默认为：0
第四位_风格G: int = 1  # 第四位默认为字母
第四位_索引G: int = 0  # 第四位的初始值默认为：""
第四位_默认GL: list = []

后缀_风格G = 0  # 后缀默认为数字
后缀_默认GL: list = []

连接符_索引G: int = 0
连接符_默认GS: str = ""

class 等级E(Enum):
    一 = 1
    二 = 2
    三 = 3
    四 = 4


配置O = 配置C()

# 例：等级 为 四级, [[等级E.四, "1", "1", "1", "a", "支杆", "一"]，]
标注GL: list[list] = []


####################################初始化#############################################
def 配置初始化F():
    global 第二位_索引G, 第三位_索引G, 第四位_风格G, 第四位_索引G, 后缀_风格G, 连接符_索引G
    配置VL: tuple = 配置O.读取配置F()

    第二位_索引G = 配置VL[0]
    第三位_索引G = 配置VL[1]
    第四位_风格G = 配置VL[2]
    第四位_索引G = 配置VL[3]
    后缀_风格G = 配置VL[4]
    连接符_索引G = 配置VL[5]


####################################事件方法#############################################


####################################界面#############################################
@ui.page(path="/")
async def _() -> None:
    # ************页眉************
    with ui.header(elevated=True).style("background-color: #3874c8"):
        ui.button(text="读取", icon="file_open", color="secondary")
        ui.button(text="保存")
        ui.space()
        ui.button(text="命名规则")

    # ************侧边栏************
    with ui.left_drawer(value=True).classes("bg-blue-grey-1").style("width: 150px!important;"):
        ui.button(text="创建顶级命名")
        ui.button(text="前")
        ui.button(text="后")
        ui.space()
        ui.button(text="粘贴")

    # ************主要内容************
    with ui.element("div"):
        with ui.card():
            ui.label("你好")


####################################入口#############################################
if __name__ in {"__main__", "__mp_main__"}:
    配置初始化F()
    ui.run(
        title=常量_标题,
        favicon=图标路径G,
        reload=True,  # 打包时，记得禁用
        port=native.find_open_port(),
        native=True,
        window_size=(1030, 760),
    )
