r"""
创建者: 阿斗是只猫
创建日期: 2025-04-09
最后编辑人: 阿斗是只猫
最后编辑时间: 2025-05-02
说明:

    如有问题或建议，请联系微信公众号：【阿斗的小窝】

    Copyright (c) 2025 by 阿斗是只猫, All Rights Reserved.
"""

# 导入常用模块
from dataclasses import dataclass
from encodings import mac_greek
from enum import IntEnum
from pathlib import Path
from pprint import pprint

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


class 等级E(IntEnum):
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
            ui.button(text="粘贴", on_click=粘贴F)

            ui.separator()
            ui.label("****CAD****")
            ui.button(text="绑定CAD")
            ui.button(text="标记")
            ui.button(text="清空")
            ui.button(text="输入")

            ui.separator()
            ui.label("****图片****")
            ui.button(text="选择图片")
            ui.button(text="标记")
            ui.button(text="输入")

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
        self.等级VE: 等级E = 等级V
        self.零件名V: str = 零件名VS
        self.后缀V: str = 后缀V
        self.重名次数V: int = 重名次数V

        self.第一位_索引V: int = 第一位_索引V
        self.第二位_索引V: int = 第二位_索引V
        self.第三位_索引V: int = 第三位_索引V
        self.第四位_索引V: int = 第四位_索引V
        self.刷新次数V: int = 0

        self._等级配置V = {
            等级E.一: {"颜色": 常量_颜色["一级"], "位置": 常量_一级_位置},
            等级E.二: {"颜色": 常量_颜色["二级"], "位置": 常量_二级_位置},
            等级E.三: {"颜色": 常量_颜色["三级"], "位置": 常量_三级_位置},
            等级E.四: {"颜色": 常量_颜色["四级"], "位置": 常量_四级_位置},
        }

        self.获取等级配置F()
        self.生成文本F()

        self.是否_checkbox_选中: bool = False

        with (
            self,
            ui.row().classes("rounded-full space-x-0.5 p-0.5 m-0.5 items-center").style("width: fit-content;"),
        ):
            self.动态刷新F()

    # ui.state() 和  @ui.refreshable 实现了状态持久化和UI自动刷新。
    @ui.refreshable
    def 动态刷新F(self):
        ui.element("div").style(f"width: {self.配置V['位置']}px;")
        with ui.card().tight().style(f"background-color: {self.配置V['颜色']}"):
            with ui.row().classes("rounded-full space-x-0.5 p-0.5 m-0.5 items-center").style("width: fit-content;"):
                (
                    ui.checkbox()
                    .bind_value(self, "是否_checkbox_选中")
                    .on_value_change(self.选择标签F)
                    .classes("m-0 p-0 h-4 w-4 shrink-0")
                )
                ui.label(self.文本V).classes("m-0 p-0 shrink-0").on("click", lambda: self.更改F())
                ui.button(icon="add_circle", on_click=添加标签F).classes(
                    "m-0 p-0 h-4 w-4 rounded-full bg-transparent border-none text-xs min-h-0 min-w-0"
                ).style("min-width: 0 !important; min-height: 0 !important")
                ui.button(icon="cancel", on_click=self.删除F).classes(
                    "m-0 p-0 h-4 w-4 rounded-full bg-transparent border-none text-xs min-h-0 min-w-0"
                ).style("min-width: 0 !important; min-height: 0 !important")

        self.刷新次数V += 1
        pprint(f"""
            ***************************标签对象-动态刷新***************************
            刷新次数：{self.刷新次数V}
            索引：{self.序号V}
            等级：{self.等级VE}
            text：{self.文本V}
            位置V：{self.配置V["位置"]}
            color：{self.配置V["颜色"]}
            ########################################
            """)

    def 选择标签F(self):
        if self.是否_checkbox_选中:
            生成器O.选择标签F(self.序号V)

    async def 更改F(self):
        if self.是否_checkbox_选中:
            await 生成器O.重输_零件名F()

    def 删除F(self):
        if self.是否_checkbox_选中:
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

    def 获取等级配置F(self):
        self.配置V = self._等级配置V.get(self.等级VE)
        if not self.配置V:
            self.配置V = self._等级配置V.get(等级E.一)
            ui.notify(f"不支持的等级: {self.等级VE}")

    def 刷新标签F(self):
        self.获取等级配置F()
        self.生成文本F()
        self.动态刷新F.refresh()


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
    生成器O.添加标签F(text)


def 提升等级F():
    if 当前标签G > 0:
        if 等级E.一 == 等级G:
            ui.notify("当前标签已为最高级别，无法提升！")
        elif 等级E.二 == 等级G:
            生成器O.修改标签等级F(当前标签G, 等级E.一)
        elif 等级E.三 == 等级G:
            生成器O.修改标签等级F(当前标签G, 等级E.二)
        elif 等级E.四 == 等级G:
            生成器O.修改标签等级F(当前标签G, 等级E.三)
    else:
        ui.notify("第一个元素无法提升等级！")


def 降低等级F():
    if 当前标签G > 0:  # 排除第一个元素
        if 等级E.一 == 等级G:
            生成器O.修改标签等级F(当前标签G, 等级E.二)
        elif 等级E.二 == 等级G:
            生成器O.修改标签等级F(当前标签G, 等级E.三)
        elif 等级E.三 == 等级G:
            生成器O.修改标签等级F(当前标签G, 等级E.四)
        elif 等级E.四 == 等级G:
            ui.notify("降低等级F：当前标签已为最低级别，无法降低！")
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
        self.是否_超出索引V: bool = False

    def 选择标签F(self, 序号V):
        global 当前标签G, 等级G
        # TODO 当前标签G在进来前就被改了
        self.前_标签序号V = 当前标签G
        当前标签G = 序号V

        等级G = self.标注VL[当前标签G].等级VE

        if self._长度V > 1:
            self.标注VL[self.前_标签序号V].是否_checkbox_选中 = False

        print(f"""
            *******************************选择标签************************************
                前_标签-索引：{self.前_标签序号V}，checkbox.value：{self.标注VL[self.前_标签序号V].是否_checkbox_选中}
                ----------当前
                当前标签-索引：{当前标签G}， checkbox.value：{self.标注VL[当前标签G].是否_checkbox_选中}
                当前标签名称：{self.标注VL[当前标签G].文本V}
                等级G：{等级G}
            ####################################################################
            """)

    def 删除标签F(self):
        global 当前标签G

        生成区域G.remove(当前标签G)
        self.标注VL.pop(当前标签G)

        if self._长度V > 0:
            i: int = 当前标签G
            while i < self._长度V:
                self.标注VL[i].序号V = i

                # 修改后缀，删除的零件名可能与后面某个重复
                if self.标注VL[i].重名次数V > 0:
                    self.修改零件名F(i, self.标注VL[i].零件名VS)
                i += 1

            self.标注VL[当前标签G].是否_checkbox_选中 = True
        else:
            self.前_标签序号V = 0
            当前标签G = 0

    def 修改标签等级F(self, 选定序号V: int, 目标等级VE: 等级E):
        # 降低标签等级
        if 目标等级VE > self.标注VL[选定序号V].等级VE:
            # 从一级将为二级
            if 等级E.二 == 目标等级VE:
                # 首先需要查看是否有空位
                if self.标注VL[选定序号V - 1].第二位_索引V < self.第二位_长度V - 1:
                    self.标注VL[选定序号V].第一位_索引V = self.标注VL[选定序号V - 1].第一位_索引V
                    self.标注VL[选定序号V].第二位_索引V = self.标注VL[选定序号V - 1].第二位_索引V + 1

                    # 修改成功后，修改等级；修改不成功则不动
                    self.修改等级F(目标等级VE, 选定序号V)

                    # 某个标签从一级降维二级，那么就需要修改后面所有标签的的第一位索引
                    i = 选定序号V + 1
                    while i < self._长度V:
                        self.标注VL[i].第一位_索引V -= 1
                        self.更新标签F(i)
                        i += 1
                else:
                    ui.notify("修改标签等级F-降低等级：第二位位置已满，无法降低等级")

            # 从二级降为三级
            elif 等级E.三 == 目标等级VE:
                if self.标注VL[选定序号V].第二位_索引V > 命名O.第二位_初始索引V + 1:  # 排除类似于110这种
                    if self.标注VL[选定序号V - 1].第三位_索引V < self.第三位_长度V - 1:
                        self.标注VL[选定序号V].第一位_索引V = self.标注VL[选定序号V - 1].第一位_索引V
                        self.标注VL[选定序号V].第二位_索引V = self.标注VL[选定序号V - 1].第二位_索引V
                        self.标注VL[选定序号V].第三位_索引V = self.标注VL[选定序号V - 1].第三位_索引V + 1

                        self.修改等级F(目标等级VE, 选定序号V)

                        self.修改_标号重标注F(等级E.二, 等级E.一)
                    else:
                        ui.notify("修改标签等级F-降低等级：第三位位置已满，无法降低等级")
                else:
                    ui.notify("修改标签等级F-降低等级：当前标签为第二位的领头标签，无法降低等级")

            # 从三级降为四级
            elif 等级E.四 == 目标等级VE:
                if self.标注VL[选定序号V].第三位_索引V > 命名O.第三位_初始索引V + 1:
                    if self.标注VL[选定序号V - 1].第四位_索引V < self.第四位_长度V - 1:
                        self.标注VL[选定序号V].第一位_索引V = self.标注VL[选定序号V - 1].第一位_索引V
                        self.标注VL[选定序号V].第二位_索引V = self.标注VL[选定序号V - 1].第二位_索引V
                        self.标注VL[选定序号V].第三位_索引V = self.标注VL[选定序号V - 1].第三位_索引V
                        self.标注VL[选定序号V].第四位_索引V = self.标注VL[选定序号V - 1].第四位_索引V + 1

                        self.修改等级F(目标等级VE, 选定序号V)

                        self.修改_标号重标注F(等级E.三, 等级E.二)
                    else:
                        ui.notify("修改标签等级F-降低等级：第四位位置已满，无法降低等级")
                else:
                    ui.notify("修改标签等级F-降低等级：当前标签为第三位的领头标签，无法降低等级")

        # 提高标签等级
        else:
            # 从二级升为一级
            if 等级E.一 == 目标等级VE:
                # 查看第一位的索引是否有空位，避免第一位索引已经到极限，导致超出索引范围的问题
                if self.第一位_索引V < self.第一位_长度V - 1:
                    self.标注VL[选定序号V].第一位_索引V = self.标注VL[选定序号V - 1].第一位_索引V + 1
                    self.标注VL[选定序号V].第二位_索引V = 命名O.第二位_初始索引V
                    self.标注VL[选定序号V].第三位_索引V = 命名O.第三位_初始索引V
                    self.标注VL[选定序号V].第四位_索引V = 命名O.第四位_初始索引V

                    self.修改等级F(目标等级VE, 选定序号V)

                    # 当前标签之后的所有标签第一位索引+1，即向后移一位
                    i = 选定序号V + 1
                    while i < self._长度V:
                        self.标注VL[i].第一位_索引V += 1
                        self.更新标签F(i)
                        i += 1

                    # 修改子标签的等级
                    j = 选定序号V + 1
                    while j < self._长度V:
                        if 等级E.二 == self.标注VL[j].等级VE or 等级E.一 == self.标注VL[j].等级VE:
                            break
                        elif 等级E.三 == self.标注VL[j].等级VE:
                            self.修改标签等级F(j, 等级E.二)
                        elif 等级E.四 == self.标注VL[j].等级VE:
                            self.修改标签等级F(j, 等级E.三)

                        j += 1

                    # 修改后续标签的第二位索引，直到遇到一级标签截至
                    m = 选定序号V + 1
                    while m < self._长度V:
                        if 等级E.一 == self.标注VL[m].等级VE:
                            break

                        self.标注VL[m].第二位_索引V -= 1
                        self.更新标签F(m)

                        m += 1

                else:
                    ui.notify("修改标签等级F-提高等级：第一位位置已满，无法提升等级")

            # 从三级升为二级
            elif 等级E.二 == 目标等级VE:
                if self.计数F(等级E.二, 等级E.一) < self.第二位_长度V:
                    self.标注VL[选定序号V].第一位_索引V = self.标注VL[选定序号V - 1].第一位_索引V
                    self.标注VL[选定序号V].第二位_索引V = self.标注VL[选定序号V - 1].第二位_索引V + 1
                    self.标注VL[选定序号V].第三位_索引V = 命名O.第三位_初始索引V
                    self.标注VL[选定序号V].第四位_索引V = 命名O.第四位_初始索引V

                    self.修改等级F(目标等级VE, 选定序号V)

                    # 当前标签之后的所有标签第二位索引+1，即向后移一位
                    i = 选定序号V + 1
                    while i < self._长度V:
                        if 等级E.一 == self.标注VL[j].等级VE:
                            break

                        self.标注VL[i].第二位_索引V += 1
                        self.更新标签F(i)
                        i += 1

                    # 修改子标签的第三位_索引V
                    j = 选定序号V + 1
                    while j < self._长度V:
                        if 等级E.二 == self.标注VL[j].等级VE or 等级E.一 == self.标注VL[j].等级VE:
                            break

                        self.标注VL[j].第三位_索引V = self.标注VL[j - 1].第三位_索引V + 1
                        self.更新标签F(j)
                        j += 1

                else:
                    ui.notify("修改标签等级F-提高等级：第二位位置已满，无法提升等级")

            # 从四级升为三级
            elif 等级E.三 == 目标等级VE:
                if self.计数F(等级E.三, 等级E.二) < self.第三位_长度V:
                    self.标注VL[选定序号V].第一位_索引V = self.标注VL[选定序号V - 1].第一位_索引V
                    self.标注VL[选定序号V].第二位_索引V = self.标注VL[选定序号V - 1].第二位_索引V
                    self.标注VL[选定序号V].第三位_索引V = self.标注VL[选定序号V - 1].第三位_索引V + 1
                    self.标注VL[选定序号V].第四位_索引V = 命名O.第四位_初始索引V

                    self.修改等级F(目标等级VE, 选定序号V)

                    # 当前标签之后的所有标签第三位索引+1，即向后移一位
                    i = 选定序号V + 1
                    while i < self._长度V:
                        if 等级E.二 == self.标注VL[j].等级VE or 等级E.一 == self.标注VL[i].等级VE:
                            break

                        self.标注VL[i].第三位_索引V += 1
                        self.更新标签F(i)
                        i += 1

                    # 修改子标签的第四位_索引V
                    j = 选定序号V + 1
                    while j < self._长度V:
                        if 等级E.四 == self.标注VL[j].等级VE:
                            self.标注VL[j].第四位_索引V = self.标注VL[j - 1].第三位_索引V + 1
                            self.更新标签F(j)
                        else:
                            break

                        j += 1

                else:
                    ui.notify("修改标签等级F-提高等级：第三位位置已满，无法提升等级")

        self.更新标签F(选定序号V)

        pprint(f"""
**************************标签生成器C--修改标签等级F**********************
标注GL：{标注GL}
######################################
            """)

    # 计算同级标签的数量，用于与某级的长度进行比较
    def 计数F(self, 目标等级VE: 等级E, 截至等级VE: 等级E) -> int:
        count: int = 0
        if 等级E.二 == 目标等级VE:
            count = self.标注VL[当前标签G].第二位_索引V
        elif 等级E.三 == 目标等级VE:
            count = self.标注VL[当前标签G].第三位_索引V

        i = 当前标签G + 1
        while i < self._长度V:
            if 目标等级VE == self.标注VL[i].等级VE:
                count += 1
            elif 截至等级VE == self.标注VL[i].等级VE:
                break

            i += 1

        return count

    def 修改_标号重标注F(self, 目标等级VE: 等级E, 截至等级VE: 等级E):
        i = 当前标签G + 1
        while i < self._长度V:
            if self.标注VL[i].等级VE == 截至等级VE:
                break  # 循环到截至等级的标签，就不需要在修改了
            else:
                if 等级E.二 == 目标等级VE and self.标注VL[i].第二位_索引V > 0:
                    self.标注VL[i].第二位_索引V -= 1
                elif 等级E.三 == 目标等级VE and self.标注VL[i].第三位_索引V > 0:
                    self.标注VL[i].第三位_索引V -= 1
                elif 等级E.四 == 目标等级VE and self.标注VL[i].第四位_索引V > 0:
                    self.标注VL[i].第四位_索引V -= 1

                self.更新标签F(i)
            i += 1

    def 修改等级F(self, 目标等级VE: 等级E, 序号V: int):
        global 等级G
        temp = 等级G
        等级G = 目标等级VE
        self.标注VL[序号V].等级VE = 目标等级VE

        print(f"""
            *************************标签生成器C--修改等级F******************************
            已修改至目标等级：【{self.标注VL[序号V].等级VE}】
            等级G：{等级G}
            标签【{self.标注VL[序号V].零件名V}】的【等级G】已由【{temp}】修改为【{等级G}】
            ############################################################
            """)

    def 更新标签F(self, 序号V: int):
        global 标注GL
        self.标注VL[序号V].刷新标签F()

        item: dict = [
            self.标注VL[序号V].等级VE,
            self.标注VL[序号V].第一位V,
            self.标注VL[序号V].第二位V,
            self.标注VL[序号V].第三位V,
            self.标注VL[序号V].第四位V,
            self.标注VL[序号V].零件名V,
            self.标注VL[序号V].后缀V,
        ]

        标注GL[序号V] = item

    def 添加标签F(self, 零件名V: str = "XXX"):
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
                    # TODO 修改后边的标注
                    i += 1

            self._长度V += 1
            self.标签O.是否_checkbox_选中 = True  # 选中新生成的标签，并切换当前标签G
            pprint(f"""
                *****************************添加标签F-标注G********************************
                标注GL：{标注GL}
                ####################################
                """)
            print(
                "++++++++++++++++++++++++++++++++++++++++++++++添加标签结束++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            )

    async def 重输_零件名F(self):
        输入V = await 输入框C()
        if 输入V:
            self.修改零件名F(当前标签G, 输入V)

    def 修改零件名F(self, 序号V: int, 输入V: str):
        后缀V, 重名次数V = self.零件名_重名_后缀F(输入V)
        self.标注VL[序号V].零件名V = 输入V
        self.标注VL[序号V].后缀V = 后缀V
        self.标注VL[序号V].重名次数V = 重名次数V
        self.标注VL[序号V].刷新标签F()

    def 零件名_重名_后缀F(self, 零件名V):
        result: int = 0

        if self._长度V > 0:
            i: int = 0
            while i <= 当前标签G:
                if self.标注VL[i].零件名V == 零件名V:
                    result += 1
                    print(f"后缀：{self.标注VL[i].零件名V},{零件名V},{result},{i}")
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
                    self.获取索引F()
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
                    self.获取索引F()
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
                    self.获取索引F()
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
