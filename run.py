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

from nicegui import native, ui
from tools.local_file_picker import local_file_picker
from 读写M import 配置C, 项目C
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
    常量_颜色,
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

当前标签G: int = 0


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
    global \
        第二位_索引G, \
        第三位_索引G, \
        第四位_风格G, \
        第四位_索引G, \
        后缀_风格G, \
        连接符_索引G, \
        第四位_默认GL, \
        后缀_默认GL, \
        连接符_默认GS

    配置VL: tuple = 配置O.读取配置F()

    第二位_索引G = 配置VL[0]
    第三位_索引G = 配置VL[1]
    第四位_风格G = 配置VL[2]
    第四位_索引G = 配置VL[3]
    后缀_风格G = 配置VL[4]
    连接符_索引G = 配置VL[5]

    第四位_默认GL = 常量_第四位[第四位_风格G]
    后缀_默认GL = 常量_后缀[后缀_风格G]
    连接符_默认GS = 常量_连接符[连接符_索引G]


####################################界面#############################################
@ui.page(path="/")
async def _() -> None:
    # ************页眉************
    with ui.header(elevated=True).style("background-color: #3874c8"):
        ui.button(text="读取", icon="file_open", on_click=读取文件F, color="secondary")
        ui.button(text="保存", on_click=保存文件F)
        ui.space()
        ui.button(text="命名规则", on_click=lambda: 命名规则面板C())

    # ************侧边栏************
    with ui.left_drawer(value=True).props("width=150").classes("bg-blue-grey-1"):
        with ui.column():
            ui.button(text="创建顶级命名")
            ui.button(text="前")
            ui.button(text="后")
            ui.space()
            ui.button(text="粘贴")

    # ************主要内容************
    with ui.card().style("background-color: #ff0000;"):
        with ui.column().classes("w-full"):
            标签C(1, "你好")

class 命名规则面板C(ui.dialog):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        with self, ui.card().classes("p-4"):
            ui.label("**********命名规则**********")

            with ui.row().classes("w-full"):
                ui.label("第二位初始值：")
                self.toggle1 = ui.toggle({0: "无", 1: "0"}, value=1)

            with ui.row().classes("w-full"):
                ui.label("第三位初始值：")
                self.toggle2 = ui.toggle({0: "无", 1: "0"}, value=1)

            with ui.row().classes("w-full"):
                ui.label("第四位风格：")
                self.toggle3 = ui.toggle({0: "数字", 1: "字母"}, value=1)

            with ui.row().classes("w-full"):
                ui.label("第四位初始值：")
                self.toggle4 = ui.toggle({0: "无", 1: "0/a"}, value=0)

            with ui.row().classes("w-full"):
                ui.label("后缀风格：")
                self.toggle5 = ui.toggle({0: "中文数字", 1: "罗马数字"}, value=0)

            with ui.row().classes("w-full"):
                ui.label("连接符类型")
                self.toggle6 = ui.toggle({0: "无", 1: "-"}, value=0)

            with ui.row().classes("w-full justify-end"):
                ui.button("关闭", on_click=self.close).props("outline")
                ui.button(text="确定", on_click=self.修改配置F)

    def 修改配置F(self):
        global \
            第二位_索引G, \
            第三位_索引G, \
            第四位_风格G, \
            第四位_索引G, \
            后缀_风格G, \
            连接符_索引G, \
            第四位_默认GL, \
            后缀_默认GL, \
            连接符_默认GS

        第二位_索引G = self.toggle1.value  # type: ignore
        第三位_索引G = self.toggle2.value  # type: ignore
        第四位_风格G = self.toggle3.value  # type: ignore
        第四位_索引G = self.toggle4.value  # type: ignore
        后缀_风格G = self.toggle5.value  # type: ignore
        连接符_索引G = self.toggle6.value  # type: ignore

        第四位_默认GL = 常量_第四位[第四位_风格G]
        后缀_默认GL = 常量_后缀[后缀_风格G]  # type: ignore
        连接符_默认GS = 常量_连接符[连接符_索引G]

        配置O.写入配置F(第二位_索引G, 第三位_索引G, 第四位_风格G, 第四位_索引G, 后缀_风格G, 连接符_索引G)  # type: ignore


class 标签C(ui.card):
    def __init__(self, 序号V: int, text: str = "  ") -> None:
        super().__init__()
        self.tight()

        self.序号V = 序号V

        with self, ui.row().classes("rounded-full space-x-0.5 p-0.5 m-0.5 items-center").style("width: fit-content"):
            # 调整 checkbox 样式
            self.checkbox = ui.checkbox(value=False, on_change=lambda: self.更改当前标签F()).classes(
                "m-0 p-0 h-4 w-4 shrink-0"
            )
            self.lable = ui.label(text).classes("m-0 p-0 shrink-0").on("click", lambda: self.更改F())
            # 调整按钮样式，缩小图标大小
            ui.button(icon="add_circle", on_click=self.新建F).classes(
                "m-0 p-0 h-4 w-4 rounded-full bg-transparent border-none text-xs min-h-0 min-w-0"
            ).style("min-width: 0 !important; min-height: 0 !important")
            ui.button(icon="cancel", on_click=self.删除F).classes(
                "m-0 p-0 h-4 w-4 rounded-full bg-transparent border-none text-xs min-h-0 min-w-0"
            ).style("min-width: 0 !important; min-height: 0 !important")

    def 更改当前标签F(self):
        global 当前标签G
        if self.checkbox.value:
            self.前_标签V = 当前标签G
            当前标签G = self.序号V
        else:
            当前标签G = self.前_标签V

        print("当前标签序号为：", 当前标签G)

    async def 更改F(self):
        global 当前标签G
        当前标签G = self.序号V
        输入V = await 输入框C()
        if 输入V:
            self.lable.set_text(输入V)

    async def 新建F(self):
        global 当前标签G
        输入V = await 输入框C()

    def 删除F(self):
        pass

class 输入框C(ui.dialog):
    def __init__(self, *, value: bool = False) -> None:
        super().__init__(value=value)

        with self, ui.card().classes("p-4"):
            with ui.row().classes("w-full items-center space-x-2"):
                self.输入V = ui.input(placeholder="请输入零件名").props("square outlined dense").classes("flex-1")
                ui.button(icon="check", on_click=self.更新F).classes("p-2 rounded-full bg-blue-500 text-white")

    def 更新F(self):
        self.submit(self.输入V.value)

####################################事件方法#############################################
async def 读取文件F() -> None:
    global 标注GL

    await 获取路径F()

    if 是否_sqlite(项目路径G):
        项目O = 项目C()
        标注GL = 项目O.读取F(项目路径G)
        项目O.关闭连接F()
    else:
        ui.notify("你选中的文件不是db文件，请重新选择！")


async def 保存文件F() -> None:
    await 获取路径F()

    if 项目路径G.is_dir():
        项目O = 项目C()
        项目O.保存F(项目路径G, 标注GL)
        项目O.关闭连接F()
    else:
        ui.notify("你选中的文件不是目录，请重新选择！")

async def 获取路径F() -> None:
    global 项目路径G
    temp = await local_file_picker("~", multiple=True)
    项目路径G = temp[0]
    print("读取到的文件或目录路径：", 项目路径G)


def 是否_sqlite(path: Path):
    扩展名V: str = path.suffix.lower()
    return 扩展名V in [".sqlite", ".sqlite3", ".db"]


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
