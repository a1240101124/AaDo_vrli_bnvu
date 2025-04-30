r"""
创建者: 阿斗是只猫
创建日期: 2025-04-09
最后编辑人: 阿斗是只猫
最后编辑时间: 2025-04-27
说明:

    如有问题或建议，请联系微信公众号：【阿斗的小窝】

    Copyright (c) 2025 by 阿斗是只猫, All Rights Reserved.
"""

# 导入常用模块
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from pprint import pprint
from tkinter import NO

from nicegui import native, ui
from tools.local_file_picker import local_file_picker
from 读写M import 配置C, 项目C
from 配置M import (
    常量_一级_位置,
    常量_三级_位置,
    常量_二级_位置,
    常量_后缀,
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


class 等级E(Enum):
    一 = 1
    二 = 2
    三 = 3
    四 = 4


等级G: 等级E = 等级E.一
当前标签G: int = 0  # 用于表面当前被选中的标签
生成区域G: ui.column  # 用于标签生成，方便管理
标注GL: list[list] = []  # 用于储存所有标注信息，例：等级 为 四级, [[等级E.四, "1", "1", "1", "a", "支杆", "一"]，]

第四位_默认GL: list = []
后缀_默认GL: list = []
连接符_默认GS = ""


@dataclass
class 命名C:
    第一位_初始索引V: int = 0  # 默认从索引0开始，即第一位的初始值为：1
    第二位_初始索引V: int = 1  # 第二位的初始值默认为：0
    第三位_初始索引V: int = 1  # 第三位的初始值默认为：0
    第四位_风格V: int = 1  # 第四位默认为字母
    第四位_初始索引V: int = 0  # 第四位的初始值默认为：""
    后缀_风格V: int = 0  # 后缀默认为数字
    连接符_索引V: int = 0

    def 初始化F(self):
        global 第四位_默认GL, 后缀_默认GL, 连接符_默认GS
        配置VL: tuple = 配置O.读取配置F()

        self.第二位_初始索引V = 配置VL[0]
        self.第三位_初始索引V = 配置VL[1]
        self.第四位_风格V = 配置VL[2]
        self.第四位_初始索引V = 配置VL[3]
        self.后缀_风格V = 配置VL[4]
        self.连接符_索引V = 配置VL[5]

        第四位_默认GL = 常量_第四位[self.第四位_风格V]
        后缀_默认GL = 常量_后缀[self.后缀_风格V]
        连接符_默认GS = 常量_连接符[self.连接符_索引V]

    def 更新配置F(self, value_1, value_2, value_3, value_4, value_5, value_6):
        global 第四位_默认GL, 后缀_默认GL, 连接符_默认GS

        self.第二位_初始索引V = value_1
        self.第三位_初始索引V = value_2
        self.第四位_风格V = value_3
        self.第四位_初始索引V = value_4
        self.后缀_风格V = value_5
        self.连接符_索引V = value_6

        第四位_默认GL = 常量_第四位[self.第四位_风格V]
        后缀_默认GL = 常量_后缀[self.后缀_风格V]
        连接符_默认GS = 常量_连接符[self.连接符_索引V]

        配置O.写入配置F(
            self.第二位_初始索引V,
            self.第三位_初始索引V,
            self.第四位_风格V,
            self.第四位_初始索引V,
            self.后缀_风格V,
            self.连接符_索引V,
        )


####################################主界面#############################################
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
            ui.button(text="新建", on_click=添加标签F)
            ui.button(text="前", on_click=提升等级F)
            ui.button(text="后", on_click=降低等级F)
            ui.space()
            ui.button(text="粘贴", on_click=粘贴F)

    # ************主要内容************
    with ui.card().style("width: 82vw; height: 85vh;"):
        global 生成区域G
        生成区域G = ui.column(align_items="start").classes("w-full")


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
        命名O.更新配置F(
            self.toggle1.value,
            self.toggle2.value,
            self.toggle3.value,
            self.toggle4.value,
            self.toggle5.value,
            self.toggle6.value,
        )


class 标签C(ui.element):
    def __init__(
        self,
        序号V: int,
        等级V: 等级E,
        第一位_索引V: int,
        第二位_索引V: int,
        第三位_索引V: int,
        第四位_索引V: int,
        零件名VS: int = "XXX",
        后缀V: str = "",
        重名次数V: int = 0,
    ) -> None:
        super().__init__(tag="div")
        self.序号V = 序号V  # 用于存储自身的序号
        self.等级V: 等级E = 等级V
        self.零件名V: str = 零件名VS
        self.后缀V: str = 后缀V
        self.重名次数V: int = 重名次数V

        self.第一位_索引V: int = 第一位_索引V
        self.第二位_索引V: int = 第二位_索引V
        self.第三位_索引V: int = 第三位_索引V
        self.第四位_索引V: int = 第四位_索引V

        self._等级配置V = {
            等级E.一: {"颜色": 常量_颜色["一级"], "位置": 常量_一级_位置},
            等级E.二: {"颜色": 常量_颜色["二级"], "位置": 常量_二级_位置},
            等级E.三: {"颜色": 常量_颜色["三级"], "位置": 常量_三级_位置},
            等级E.四: {"颜色": 常量_颜色["四级"], "位置": 常量_四级_位置},
        }

        self.获取等级配置F()
        self.生成文本F()

        pprint(
            f"当前标的签序号：【{self.序号V}】，等级：【{self.等级V}】,文本：【{self.文本V}】，它的配置：{self.配置V}"
        )

        with self, ui.row().classes("rounded-full space-x-0.5 p-0.5 m-0.5 items-center").style("width: fit-content;"):
            ui.element("div").style(f"width: {self.配置V['位置']}px;")
            with ui.card().tight().style(f"background-color: {self.配置V['颜色']}"):
                with ui.row().classes("rounded-full space-x-0.5 p-0.5 m-0.5 items-center").style("width: fit-content;"):
                    self.checkbox = ui.checkbox(value=False, on_change=lambda: self.选择标签F()).classes(
                        "m-0 p-0 h-4 w-4 shrink-0"
                    )
                    self.lable = ui.label(self.文本V).classes("m-0 p-0 shrink-0").on("click", lambda: self.更改F())
                    ui.button(icon="add_circle", on_click=添加标签F).classes(
                        "m-0 p-0 h-4 w-4 rounded-full bg-transparent border-none text-xs min-h-0 min-w-0"
                    ).style("min-width: 0 !important; min-height: 0 !important")
                    ui.button(icon="cancel", on_click=self.删除F).classes(
                        "m-0 p-0 h-4 w-4 rounded-full bg-transparent border-none text-xs min-h-0 min-w-0"
                    ).style("min-width: 0 !important; min-height: 0 !important")

    def 选择标签F(self):
        if self.checkbox.value:
            生成器O.选择标签F(self.序号V)

    async def 更改F(self):
        if self.checkbox.value:
            生成器O.重输_零件名F()

    def 删除F(self):
        if self.checkbox.value:
            生成器O.删除标签F()

    def 生成文本F(self):
        self.第一位V = 常量_第一位[self.第一位_索引V]
        self.第二位V = 常量_第二位[self.第二位_索引V]
        self.第三位V = 常量_第三位[self.第三位_索引V]
        self.第四位V = 第四位_默认GL[self.第四位_索引V]

        self.文本V = (
            self.第一位V
            + 连接符_默认GS
            + self.第二位V
            + 连接符_默认GS
            + self.第三位V
            + 连接符_默认GS
            + self.第四位V
            + "、"
            + self.零件名V
            + self.后缀V
        )
        print(f"生成文本：{self.文本V}")

    def 获取等级配置F(self):
        self.配置V = self._等级配置V.get(self.等级V)
        if not self.配置V:
            self.配置V = self._等级配置V.get(等级E.一)
            ui.notify(f"不支持的等级: {self.等级V}")


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


async def 添加标签F():
    global 当前标签G
    text = await 输入框C()
    当前标签O = 生成器O.添加标签F(text)
    if 当前标签O:
        当前标签G = 当前标签O.序号V


def 提升等级F():
    if 当前标签G > 0:
        if 等级E.一 == 等级G:
            ui.notify("当前标签已为最高级别，无法提升！")
        elif 等级E.二 == 等级G:
            生成器O.修改标签等级F(等级E.一)
        elif 等级E.三 == 等级G:
            生成器O.修改标签等级F(等级E.二)
        elif 等级E.四 == 等级G:
            生成器O.修改标签等级F(等级E.三)
    else:
        ui.notify("第一个元素无法提升等级！")


def 降低等级F():
    if 当前标签G > 0:
        if 等级E.一 == 等级G:
            生成器O.修改标签等级F(等级E.二)
        elif 等级E.二 == 等级G:
            生成器O.修改标签等级F(等级E.三)
        elif 等级E.三 == 等级G:
            生成器O.修改标签等级F(等级E.四)
        elif 等级E.四 == 等级G:
            ui.notify("当前标签已为最低级别，无法降低！")
    else:
        ui.notify("第一个元素无法降低等级！")


def 粘贴F():
    pass


####################################生成器#############################################
class 标签生成器C:
    def __init__(self):
        self.标注VL: list[标签C] = []  # 储存所有标签类
        self._长度V = 0  # 用于记录 标注VL 列表的长度
        self.第一位_长度V = len(常量_第一位)
        self.第二位_长度V = len(常量_第二位)
        self.第三位_长度V = len(常量_第三位)
        self.第四位_长度V = len(第四位_默认GL)
        self.后缀_长度V = len(后缀_默认GL)

        self.第一位_索引V: int = 命名O.第一位_初始索引V
        self.第二位_索引V: int = 命名O.第二位_初始索引V
        self.第三位_索引V: int = 命名O.第三位_初始索引V
        self.第四位_索引V: int = 命名O.第四位_初始索引V

        self.前_标签序号V: int = 0  # 用于表明上一个被选中的标签

    def 选择标签F(self, 序号V):
        global 当前标签G

        self.前_标签序号V = 当前标签G
        当前标签G = 序号V

        if 当前标签G > 0:
            self.标注VL[self.前_标签序号V].checkbox.value = False

        print("当前标签序号为：", 当前标签G)

    def 删除标签F(self):
        global 当前标签G

        生成区域G.remove(当前标签G)
        self.标注VL.pop(当前标签G)

        if self._长度V > 0:
            i: int = 当前标签G
            while i < self._长度V:
                self.标注VL[i].序号V = i

                # 修改后缀，删除的可能与后面某个重复
                if self.标注VL[i].重名次数V > 0:
                    self.修改零件名F(i, self.标注VL[i].零件名VS)
                i += 1

            self.标注VL[当前标签G].checkbox.value = True
            self.前_标签序号V = 当前标签G
        else:
            self.前_标签序号V = 0
            当前标签G = 0

    def 修改标签等级F(self, 等级V: 等级E):
        # 降低标签等级
        if self.标注VL[当前标签G].等级V < 等级E:
            if 等级E.二 == 等级V:
                self.标注VL[当前标签G].第一位_索引V = self.标注VL[当前标签G - 1].第一位_索引V
                self.标注VL[当前标签G].第二位_索引V += 1
            elif 等级E.三 == 等级V:
                self.标注VL[当前标签G].第一位_索引V = self.标注VL[当前标签G - 1].第一位_索引V
                self.标注VL[当前标签G].第二位_索引V = self.标注VL[当前标签G - 1].第二位_索引V
                self.标注VL[当前标签G].第三位_索引V += 1
            elif 等级E.四 == 等级V:
                self.标注VL[当前标签G].第一位_索引V = self.标注VL[当前标签G - 1].第一位_索引V
                self.标注VL[当前标签G].第二位_索引V = self.标注VL[当前标签G - 1].第二位_索引V
                self.标注VL[当前标签G].第三位_索引V = self.标注VL[当前标签G - 1].第三位_索引V
                self.标注VL[当前标签G].第四位_索引V += 1
        else:  # 增加标签等级
            if 等级E.一 == 等级V:
                self.标注VL[当前标签G].第一位_索引V = self.标注VL[当前标签G - 1].第一位_索引V + 1
                self.标注VL[当前标签G].第二位_索引V = 命名O.第二位_初始索引V
                self.标注VL[当前标签G].第三位_索引V = 命名O.第三位_初始索引V
                self.标注VL[当前标签G].第四位_索引V = 命名O.第四位_初始索引V
            elif 等级E.二 == 等级V:
                self.标注VL[当前标签G].第一位_索引V = self.标注VL[当前标签G - 1].第一位_索引V
                self.标注VL[当前标签G].第二位_索引V = self.标注VL[当前标签G - 1].第二位_索引V + 1
                self.标注VL[当前标签G].第三位_索引V = 命名O.第三位_初始索引V
                self.标注VL[当前标签G].第四位_索引V = 命名O.第四位_初始索引V
            elif 等级E.三 == 等级V:
                self.标注VL[当前标签G].第一位_索引V = self.标注VL[当前标签G - 1].第一位_索引V
                self.标注VL[当前标签G].第二位_索引V = self.标注VL[当前标签G - 1].第二位_索引V
                self.标注VL[当前标签G].第三位_索引V = self.标注VL[当前标签G - 1].第三位_索引V + 1
                self.标注VL[当前标签G].第四位_索引V = 命名O.第四位_初始索引V
        # TODO 要对后面的标签索引进行更改
        # 对当前标签进行更新
        self.标注VL[当前标签G].等级V = 等级V
        self.标注VL[当前标签G].获取等级配置F()
        self.标注VL[当前标签G].生成文本F()
        self.标注VL[当前标签G].update()

    def 添加标签F(self, 零件名V: str = "XXX") -> 标签C:
        """生成指定等级的标签组件"""

        global 等级G, 标注GL

        if not self.是否_超出索引V:
            self.获取索引F()
            后缀V, 重名次数V = self.零件名_重名_后缀F(零件名V)

            # 如果在尾部添加新建新标签
            if self._长度V == 0 or self._长度V - 1 == 当前标签G:
                self.标签O = 标签C(
                    序号V=self._长度V,
                    等级V=等级G,
                    零件名VS=零件名V,
                    第一位_索引V=self.第一位_索引V,
                    第二位_索引V=self.第二位_索引V,
                    第三位_索引V=self.第三位_索引V,
                    第四位_索引V=self.第四位_索引V,
                    后缀V=后缀V,
                    重名次数V=重名次数V,
                )
                self.标签O.move(target_container=生成区域G, target_index=self._长度V)
                self.标注VL.append(self.标签O)
                标注GL.append(
                    [
                        等级G,
                        self.标签O.第一位V,
                        self.标签O.第二位V,
                        self.标签O.第三位V,
                        self.标签O.第四位V,
                        零件名V,
                        后缀V,
                    ]
                )
            # 如果在中间添加新建新标签
            else:
                self.标签O = 标签C(
                    序号V=当前标签G + 1,
                    等级V=等级G,
                    零件名VS=零件名V,
                    第一位_索引V=self.第一位_索引V,
                    第二位_索引V=self.第二位_索引V,
                    第三位_索引V=self.第三位_索引V,
                    第四位_索引V=self.第四位_索引V,
                    后缀V=后缀V,
                    重名次数V=重名次数V,
                )
                self.标签O.move(target_container=生成区域G, target_index=当前标签G + 1)
                self.标注VL.insert(当前标签G + 1, self.标签O)
                标注GL.insert(
                    当前标签G + 1,
                    [
                        等级G,
                        self.标签O.第一位V,
                        self.标签O.第二位V,
                        self.标签O.第三位V,
                        self.标签O.第四位V,
                        零件名V,
                        后缀V,
                    ],
                )

                # 更改后续标签的序号
                i = 当前标签G + 2
                while i <= self._长度V:
                    self.标注VL[i].序号V += 1
                    # 修改后缀，后边的标签可能与新加的重名，所以需要修改
                    self.修改零件名F(i, self.标注VL[i].零件名VS)
                    i += 1

            self.标签O.checkbox.value = True  # 选中新生成的标签，并切换当前标签G
            pprint(f"标注G:{标注GL}")
            self._长度V += 1
            return self.标签O

        return None

    async def 重输_零件名F(self):
        输入V = await 输入框C()
        if 输入V:
            self.修改零件名F(当前标签G, 输入V)

    def 修改零件名F(self, 序号V: int, 输入V: str):
        self.标注VL[序号V].零件名V = 输入V
        后缀V, 重名次数V = self.零件名_重名_后缀F(输入V)
        self.标注VL[序号V].后缀V = 后缀V
        self.标注VL[序号V].重名次数V = 重名次数V
        文本V = self.标注VL[序号V].生成文本F()
        self.标注VL[序号V].lable.set_text(文本V)

    def 零件名_重名_后缀F(self, 零件名V):
        result: int = 0
        if self._长度V > 0:
            i: int = 0
            while i <= 当前标签G:
                if self.标注VL[i].零件名V == 零件名V:
                    result += 1
                i += 1

        if result < self.后缀_长度V:
            后缀V = 后缀_默认GL[result]
        else:
            ui.notify("""
                    重复的零件名太多了，已经超出上限！
                    源自：标签生成器C.零件名_重名_后缀F
                    """)
        return 后缀V, result

    def 获取索引F(self):
        global 等级G
        self.是否_超出索引V: bool = False
        if self._长度V > 0:
            if 等级E.一 == 等级G:
                if self.第一位_索引V < self.第一位_长度V - 1:
                    self.第一位_索引V = self.标注VL[当前标签G].第一位_索引V + 1
                    self.第二位_索引V = 命名O.第二位_初始索引V
                    self.第三位_索引V = 命名O.第三位_初始索引V
                    self.第四位_索引V = 命名O.第四位_初始索引V
                else:
                    # 当第一位索引加到头后，切换等级
                    等级G = 等级E.二
                    ui.notify("""
                        第一位已到极限！请妥善安排命名结构！
                        源自：标签生成器C.索引递增F
                        """)
            elif 等级E.二 == 等级G:
                if 命名O.第二位_初始索引V < self.第二位_长度V - 1:
                    self.第一位_索引V = self.标注VL[当前标签G].第一位_索引V
                    self.第二位_索引V = self.标注VL[当前标签G].第二位_索引V + 1
                    self.第三位_索引V = 命名O.第三位_初始索引V
                    self.第四位_索引V = 命名O.第四位_初始索引V
                else:
                    等级G = 等级E.三
                    ui.notify("""
                        第二位已到极限！请妥善安排命名结构！
                        源自：标签生成器C.索引递增F
                        """)
            elif 等级E.三 == 等级G:
                if 命名O.第三位_初始索引V < self.第三位_长度V - 1:
                    self.第一位_索引V = self.标注VL[当前标签G].第一位_索引V
                    self.第二位_索引V = self.标注VL[当前标签G].第二位_索引V
                    self.第三位_索引V = self.标注VL[当前标签G].第三位_索引V + 1
                    self.第四位_索引V = 命名O.第四位_初始索引V
                else:
                    等级G = 等级E.四
                    ui.notify("""
                        第三位已到极限！请妥善安排命名结构！
                        源自：标签生成器C.索引递增F
                        """)
            elif 等级E.四 == 等级G:
                if 命名O.第四位_初始索引V < self.第四位_长度V - 1:
                    self.第一位_索引V = self.标注VL[当前标签G].第一位_索引V
                    self.第二位_索引V = self.标注VL[当前标签G].第二位_索引V
                    self.第三位_索引V = self.标注VL[当前标签G].第三位_索引V
                    self.第四位_索引V = self.标注VL[当前标签G].第四位_索引V
                else:
                    self.是否_超出索引V = True
                    ui.notify("""
                        第四位已到极限！请妥善安排命名结构！
                        源自：标签生成器C.索引递增F
                        """)


####################################入口#############################################
if __name__ in {"__main__", "__mp_main__"}:
    配置O = 配置C()
    命名O = 命名C()
    命名O.初始化F()
    生成器O = 标签生成器C()
    ui.run(
        title=常量_标题,
        favicon=图标路径G,
        reload=True,  # 打包时，记得禁用
        port=native.find_open_port(),
        native=True,
        window_size=(1030, 760),
    )
