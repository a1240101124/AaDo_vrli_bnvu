r"""
创建者: 阿斗是只猫
创建日期: 2025-04-09
最后编辑人: 阿斗是只猫
最后编辑时间: 2025-05-12
说明:

    如有问题或建议，请联系微信公众号：【阿斗的小窝】

    Copyright (c) 2025 by 阿斗是只猫, All Rights Reserved.
"""

# 导入常用模块
import re
from dataclasses import dataclass
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
标注GL: list[
    list
] = []  # 用于储存所有标注信息，例：  标注GL：[[<等级E.一: 1>, 0, 1, 1, 0, '支杆', '', 0, '100、支杆'], "
第三方标记G: bool = False
标注GS: str = ""  # 用于记录第三方输入的标注

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


# region###################################主界面#############################################
@ui.page(path="/")
async def _() -> None:
    ui.add_head_html("""
    <style>
        :root {
            --ios-blue: #007AFF;  /* 苹果系统主蓝 */
            --ios-gray1: #F5F5F7; /* 系统浅灰背景 */
            --ios-gray2: #E5E5EA; /* 分隔线颜色 */
            --ios-text: #1D1D1F;  /* 主要文字颜色 */
        }
        body { /* 添加具体的选择器 */
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
    </style>
""")

    # ************页眉************
    with (
        ui.header(elevated=True)
        .classes("h-14")
        .style(
            "background-color: rgba(255,255,255,0.8); backdrop-filter: blur(20px);"  # 毛玻璃效果
            "border-bottom: 1px solid var(--ios-gray2);"
        )
    ):
        # 按钮样式
        btn_style = "text-color: var(--ios-text); font-weight: 500; font-size: 15px;"
        ui.button("读取", icon="file_open", on_click=读取文件F).props(f"flat {btn_style}")
        ui.button("保存", icon="save", on_click=保存文件F).props(f"flat {btn_style}")
        ui.space()
        ui.button("使用规则", icon="🛠️", on_click=使用规则F).props(f"flat {btn_style}")
        ui.button("命名规则", icon="menu", on_click=show_dialog).props(f"flat {btn_style}")

    # ************侧边栏************
    with (
        ui.left_drawer(value=True)
        .props("width=220")
        .classes("bg-[var(--ios-gray1)]")
        .style("border-right: 1px solid var(--ios-gray2);")
    ):
        with ui.column().classes("gap-2 p-3"):  # 增加内边距和间距
            # 本软件自带的主要功能
            button_style = "flat size=md justify-start full-width text-color=var(--ios-text)"
            ui.button("新建", icon="add", on_click=添加标签F).props(button_style)
            with ui.row().classes("gap-1 items-center pl-10 pr-2 my-2").style("margin-left: -1.5rem;"):
                ui.button(icon="arrow_back_ios", on_click=提升等级F).props("dense round").classes("shadow-sm")
                ui.button(icon="arrow_forward_ios", on_click=降低等级F).props("dense round").classes("shadow-sm")
            ui.button("粘贴", icon="content_copy", on_click=粘贴F).props(button_style)

            # 分隔线使用iOS风格
            ui.separator().props("color=var(--ios-gray2)")

            # 用于输入第三方的附图标记
            ui.button(text="输入其他标记", icon="edit", on_click=输入其他标记F).props(button_style).classes(
                "hover:bg-[#00000008]"
            )

            # CAD相关
            ui.separator().props("color=var(--ios-gray2)")
            ui.button(text="标记", icon="cloud_upload").props(button_style).classes("hover:bg-[#00000008]")
            ui.button(text="清空", icon="cleaning_services").props(button_style).classes("hover:bg-[#00000008]")

            # 图片相关
            ui.separator().props("color=var(--ios-gray2)")
            ui.button(text="选择图片", icon="add_photo_alternate").props(button_style).classes("hover:bg-[#00000008]")
            ui.button(text="标记", icon="cloud_upload").props(button_style).classes("hover:bg-[#00000008]")

    # ************主要内容************
    with (
        ui.card()
        .classes("m-4 rounded-xl shadow-none border")
        .style(
            "border-color: var(--ios-gray2); background: rgba(255,255,255,0.9);"
            "width: calc(100% - 2rem); height: calc(100vh - 8rem);"
        )
    ):
        global 生成区域G
        with ui.scroll_area().classes("h-full p-4"):  # 增加内边距
            生成区域G = ui.column().classes("gap-4")  # 元素间距调整为系统标准的8px倍数


class 命名规则面板C(ui.dialog):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        with (
            self,
            ui.card()
            .style("background: rgba(255,255,255,0.9)!important; border: 1px solid rgba(0,0,0,0.1)!important")
            .classes("!p-6 !rounded-2xl !shadow-lg max-w-2xl mx-auto"),
        ):
            with ui.row().classes("w-full items-center gap-4 py-3 px-4 hover:bg-gray-100/50 transition-colors"):
                ui.label("第二位初始值：").classes("text-gray-700 flex-[1] min-w-[120px]")
                self.toggle1 = ui.toggle({0: "无", 1: "0"}, value=1).classes("rounded-full bg-gray-200/50")

            with ui.row().classes("w-full items-center gap-4 py-3 px-4 hover:bg-gray-100/50 transition-colors"):
                ui.label("第三位初始值：").classes("text-gray-700 flex-[1] min-w-[120px]")
                self.toggle2 = ui.toggle({0: "无", 1: "0"}, value=1).classes("rounded-full bg-gray-200/50")

            with ui.row().classes("w-full items-center gap-4 py-3 px-4 hover:bg-gray-100/50 transition-colors"):
                ui.label("第四位风格：").classes("text-gray-700 flex-[1] min-w-[120px]")
                self.toggle3 = ui.toggle({0: "数字", 1: "字母"}, value=1).classes("rounded-full bg-gray-200/50")

            with ui.row().classes("w-full items-center gap-4 py-3 px-4 hover:bg-gray-100/50 transition-colors"):
                ui.label("第四位初始值：").classes("text-gray-700 flex-[1] min-w-[120px]")
                self.toggle4 = ui.toggle({0: "无", 1: "0/a"}, value=0).classes("rounded-full bg-gray-200/50")

            with ui.row().classes("w-full items-center gap-4 py-3 px-4 hover:bg-gray-100/50 transition-colors"):
                ui.label("后缀风格：").classes("text-gray-700 flex-[1] min-w-[120px]")
                self.toggle5 = ui.toggle({0: "中文数字", 1: "罗马数字"}, value=0).classes("rounded-full bg-gray-200/50")

            with ui.row().classes("w-full items-center gap-4 py-3 px-4 hover:bg-gray-100/50 transition-colors"):
                ui.label("连接符类型").classes("text-gray-700 flex-[1] min-w-[120px]")
                self.toggle6 = ui.toggle({0: "无", 1: "-"}, value=0).classes("rounded-full bg-gray-200/50")

            with ui.row().classes("w-full justify-end space-x-3 mt-6"):
                ui.button("关闭", on_click=self.close, color="primary").classes("px-5 py-2 text-white hover:bg-red-700")
                ui.button(text="确定", on_click=self.修改配置F, color="positive").classes(
                    "px-5 py-2 text-white hover:bg-danger-700 transition-colors"
                )

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
            ui.row().classes("rounded-full space-x-0.5 p-0.5 m-0 items-center").style("width: fit-content;"),
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
            序号V：{self.序号V}
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


# endregion ↑↑↑


# region###################################事件方法#############################################
async def 读取文件F() -> None:
    await 获取路径F()

    if 是否_sqlite(项目路径G):
        项目O = 项目C()
        标注VL: list[list] = 项目O.读取F(项目路径G)
        项目O.关闭连接F()

        # 依次创建标签
        for item in 标注VL:
            等级V = item[0]
            零件名VS = item[5]
            第一位_索引V = item[1]
            第二位_索引V = item[2]
            第三位_索引V = item[3]
            第四位_索引V = item[4]
            后缀V = item[6]
            重名次数V = item[7]
            生成器O.生成标签F(等级V, 第一位_索引V, 第二位_索引V, 第三位_索引V, 第四位_索引V, 后缀V, 重名次数V, 零件名VS)

        pprint(f"""
                *****************************读取文件F-标注G********************************
                标注GL：{标注VL}
                ####################################
                """)
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

def 使用规则F():
    with ui.dialog() as dialog, ui.card():
        ui.markdown("""
#### 🛠️ 使用规则

##### 🔧 前期准备
1. **AutoCAD 版本要求**  
   需安装 2007 及以上版本，并以管理员身份运行（首次连接时需要）。

2. **完整版安装要求**  
   必须使用完整版 AutoCAD，精简版可能缺少 COM 接口，导致 CAD 功能无法使用。
   确保CAD的字体支持汉字。

3. **操作顺序**  
   请先启动 AutoCAD，再运行本软件。
   将CAD图纸打散，确保CAD图纸中的附图标记是单行文字对象。

4. **兼容性说明**  
   已在 CAD2016 环境下测试通过，其他版本兼容性未知。


##### 📝 CAD 命名规则

###### ✅ 标准示例
`100、支杆；110、支杆一；111、支杆二；111a、支杆三；200、支杆四`

###### 📌 格式规范
1. **分隔符号**  
   - 编号与名称间使用中文顿号 `、` 分隔  
   - 条目间使用中文分号 `；` 分隔  
   - 末尾不添加任何符号

2. **命名结构**  

##### ⚠️ 注意事项
请确保输入严格符合上述规则，否则可能导致系统无法正确解析！
""").classes("text-left max-w-2xl")  # 设置最大宽度并左对齐  # noqa: W291
        ui.button("关闭", on_click=dialog.close).classes("mt-4 self-end")  # 按钮右对齐并添加间距

    dialog.open()


def show_dialog():
    dialog = 命名规则面板C()
    dialog.open()

async def 添加标签F():
    global 当前标签G
    text: str = await 输入框C()
    if text:
        生成器O.添加标签F(text)
    else:
        ui.notify("添加标签F：输入为空，请重新输入！")


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
    #  标注GL：[[<等级E.一: 1>, 0, 1, 1, 0, '支杆', '', 0, '100、支杆'], "
    temp = ""
    length = len(标注GL)

    for i, item in enumerate(标注GL):
        # 添加当前元素
        temp += item[8]
        # 除了最后一个元素，其他元素后面都添加分号
        if i < length - 1:
            temp += "；"

    ui.clipboard.write(temp)

async def 输入其他标记F():
    global 标注GS, 第三方标记G
    temp: str = ""

    temp = await 输入框C()

    valid, errors = validate_string(temp)
    print(f"输入其他标记F->验证结果: {valid}")
    if errors:
        for error in errors:
            ui.notify(f"- {error}")
    else:
        第三方标记G = True
        标注GS = valid


def validate_string(input_str):
    """用于验证第三方的附图标记是否符合规则"""
    errors = []

    try:
        # 基础类型检查
        if not isinstance(input_str, str):
            raise TypeError("输入必须为字符串类型")

        # 处理空字符串
        if not input_str.strip():
            errors.append("错误：输入字符串为空")
            return False, errors

        # 检查非法分隔符
        invalid_delimiters = re.findall(r"[;；,，]\s*[;；,，]", input_str)
        if invalid_delimiters:
            errors.append(f"错误：存在连续分隔符 {invalid_delimiters}")

        # 检查首尾分隔符
        if input_str.strip().startswith((";", "；", ",", "，")):
            errors.append("错误：字符串以分隔符开头")
        if input_str.strip().endswith((";", "；", ",", "，")):
            errors.append("错误：字符串以分隔符结尾")

        # 分割字符串（优先使用中文分号）
        if "；" in input_str:
            items = re.split(r"\s*；\s*", input_str.strip())
            if ";" in input_str:
                errors.append("警告：同时存在中文分号和英文分号，已按中文分号分割")
        elif ";" in input_str:
            items = re.split(r"\s*;\s*", input_str.strip())
            errors.append("警告：使用英文分号作为分隔符")
        else:
            errors.append("错误：未找到有效分隔符")
            return False, errors

        # 过滤空项
        items = [item for item in items if item]

        # 验证每个项的格式
        pattern = r"^\d+[a-zA-Z]?、[^;；,，]+$"
        for idx, item in enumerate(items):
            if not re.match(pattern, item):
                # 检查是否缺少顿号
                if "、" not in item:
                    errors.append(f"第 {idx + 1} 项 '{item}'：缺少顿号")
                else:
                    errors.append(f"第 {idx + 1} 项 '{item}'：格式不符合要求")

        # 如果没有错误，返回成功
        if not errors:
            return True, []
        else:
            return False, errors

    except Exception as e:
        errors.append(f"验证过程中出错: {e!s}")
        return False, errors


# endregion ↑↑↑

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

    def 修改标签等级F(self, 选定序号V: int, 修改后等级VE: 等级E):
        global 等级G
        # 降低标签等级
        if 修改后等级VE > self.标注VL[选定序号V].等级VE:
            # 将当前标签的等级从一级降为二级
            if 等级E.二 == 修改后等级VE:
                # 首先需要查看是否有空位
                if self.标注VL[选定序号V - 1].第二位_索引V < self.第二位_长度V - 1:
                    self.标注VL[选定序号V].第一位_索引V = self.标注VL[选定序号V - 1].第一位_索引V
                    self.标注VL[选定序号V].第二位_索引V = self.标注VL[选定序号V - 1].第二位_索引V + 1

                    # 修改成功后，修改等级；修改不成功则不动
                    self.修改等级F(修改后等级VE, 选定序号V)

                    # 某个标签从一级降维二级，那么就需要修改后面所有标签的的第一位索引
                    self.修改第一位索引F(选定序号V, False)

                    # 降低原二级及三级子标签的等级
                    i: int = 选定序号V + 1
                    while i < self._长度V:
                        if 等级E.一 == self.标注VL[i].等级VE:
                            break
                        elif 等级E.二 == self.标注VL[i].等级VE:
                            self.修改标签等级F(i, 等级E.三)
                        elif 等级E.三 == self.标注VL[i].等级VE:
                            self.修改标签等级F(i, 等级E.四)
                        elif 等级E.四 == self.标注VL[i].等级VE:
                            continue

                        i += 1

                    # 修改成功后，避免对子标签的等级修改，影响到全局参数【等级G】的数值
                    等级G = 修改后等级VE

                else:
                    ui.notify("修改标签等级F-降低等级：第二位位置已满，无法降低等级")

            # 将当前标签的等级从二级降为三级
            elif 等级E.三 == 修改后等级VE:
                # if self.标注VL[选定序号V].第二位_索引V > 命名O.第二位_初始索引V + 1:  # 排除类似于110这种
                if self.标注VL[选定序号V - 1].第三位_索引V < self.第三位_长度V - 1:
                    self.标注VL[选定序号V].第一位_索引V = self.标注VL[选定序号V - 1].第一位_索引V
                    self.标注VL[选定序号V].第二位_索引V = self.标注VL[选定序号V - 1].第二位_索引V
                    self.标注VL[选定序号V].第三位_索引V = self.标注VL[选定序号V - 1].第三位_索引V + 1

                    self.修改等级F(修改后等级VE, 选定序号V)

                    # 修改后续同级标签的标号
                    self.标号重标注_减F(等级E.二, 等级E.一)

                    # 将子标签（即三级标签）的等级从三级降为四级
                    j = 选定序号V + 1
                    while j < self._长度V:
                        if 等级E.一 == self.标注VL[j].等级VE or 等级E.二 == self.标注VL[j].等级VE:
                            break
                        elif 等级E.三 == self.标注VL[j].等级VE:
                            self.修改标签等级F(j, 等级E.四)
                        elif 等级E.四 == self.标注VL[j].等级VE:
                            continue

                        j += 1

                    # 避免对子标签的等级修改，影响到全局参数【等级G】的数值
                    等级G = 修改后等级VE
                else:
                    ui.notify("修改标签等级F-降低等级：第三位位置已满，无法降低等级")
                # else:
                #     ui.notify("修改标签等级F-降低等级：当前标签为第二位的领头标签，无法降低等级")

            # 将当前标签的等级从三级降为四级
            elif 等级E.四 == 修改后等级VE:
                # if self.标注VL[选定序号V].第三位_索引V > 命名O.第三位_初始索引V + 1:
                if self.标注VL[选定序号V - 1].第四位_索引V < self.第四位_长度V - 1:
                    self.标注VL[选定序号V].第一位_索引V = self.标注VL[选定序号V - 1].第一位_索引V
                    self.标注VL[选定序号V].第二位_索引V = self.标注VL[选定序号V - 1].第二位_索引V
                    self.标注VL[选定序号V].第三位_索引V = self.标注VL[选定序号V - 1].第三位_索引V
                    self.标注VL[选定序号V].第四位_索引V = self.标注VL[选定序号V - 1].第四位_索引V + 1

                    self.修改等级F(修改后等级VE, 选定序号V)

                    # 修改后续同级三级标签的标号
                    self.标号重标注_减F(等级E.三, 等级E.二)

                    # 修改子标签的第四位_索引V
                    self.增加_四级_索引F(选定序号V)
                else:
                    ui.notify("修改标签等级F-降低等级：第四位位置已满，无法降低等级")
                # else:
                #     ui.notify("修改标签等级F-降低等级：当前标签为第三位的领头标签，无法降低等级")

        # 提高标签等级
        else:
            # 将当前标签的等级从二级升为一级
            if 等级E.一 == 修改后等级VE:
                # 查看第一位的索引是否有空位，避免第一位索引已经到极限，导致超出索引范围的问题
                if self.第一位_索引V < self.第一位_长度V - 1:
                    self.标注VL[选定序号V].第一位_索引V = self.标注VL[选定序号V - 1].第一位_索引V + 1
                    self.标注VL[选定序号V].第二位_索引V = 命名O.第二位_初始索引V
                    self.标注VL[选定序号V].第三位_索引V = 命名O.第三位_初始索引V
                    self.标注VL[选定序号V].第四位_索引V = 命名O.第四位_初始索引V
                    self.修改等级F(修改后等级VE, 选定序号V)

                    # 当前标签之后的所有标签第一位索引+1，即向后移一位
                    self.修改第一位索引F(选定序号V, True)

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
                    self.增加_二级_索引F(选定序号V)

                    # 避免对子标签的等级修改，影响到全局参数【等级G】的数值
                    等级G = 修改后等级VE

                else:
                    ui.notify("修改标签等级F-提高等级：第一位位置已满，无法提升等级")

            # 将当前标签的等级从三级升为二级
            elif 等级E.二 == 修改后等级VE:
                if self.计数F(等级E.二, 等级E.一) < self.第二位_长度V:
                    self.标注VL[选定序号V].第一位_索引V = self.标注VL[选定序号V - 1].第一位_索引V
                    self.标注VL[选定序号V].第二位_索引V = self.标注VL[选定序号V - 1].第二位_索引V + 1
                    self.标注VL[选定序号V].第三位_索引V = 命名O.第三位_初始索引V
                    self.标注VL[选定序号V].第四位_索引V = 命名O.第四位_初始索引V
                    self.修改等级F(修改后等级VE, 选定序号V)

                    # 当前标签之后的所有标签第二位索引+1，即向后移一位
                    self.增加_二级_索引F(选定序号V)

                    # 将子标签（即四级标签）的等级升级为三级
                    j = 选定序号V + 1
                    while j < self._长度V:
                        if 等级E.四 == self.标注VL[j].等级VE:
                            self.修改标签等级F(j, 等级E.三)
                        else:
                            break

                        j += 1

                    # 避免对子标签的等级修改，影响到全局参数【等级G】的数值
                    等级G = 修改后等级VE

                else:
                    ui.notify("修改标签等级F-提高等级：第二位位置已满，无法提升等级")

            # 将当前标签的等级从四级升为三级
            elif 等级E.三 == 修改后等级VE:
                if self.计数F(等级E.三, 等级E.二) < self.第三位_长度V:
                    self.标注VL[选定序号V].第一位_索引V = self.标注VL[选定序号V - 1].第一位_索引V
                    self.标注VL[选定序号V].第二位_索引V = self.标注VL[选定序号V - 1].第二位_索引V
                    self.标注VL[选定序号V].第三位_索引V = self.标注VL[选定序号V - 1].第三位_索引V + 1
                    self.标注VL[选定序号V].第四位_索引V = 命名O.第四位_初始索引V

                    self.修改等级F(修改后等级VE, 选定序号V)

                    # 当前标签之后的所有标签第三位索引+1，即向后移一位
                    i = 选定序号V + 1
                    while i < self._长度V:
                        if 等级E.二 == self.标注VL[i].等级VE or 等级E.一 == self.标注VL[i].等级VE:
                            break
                        elif 等级E.三 == self.标注VL[i].等级VE:
                            self.标注VL[i].第三位_索引V = self.标注VL[i - 1].第三位_索引V + 1
                        elif 等级E.四 == self.标注VL[i].等级VE:
                            self.标注VL[i].第三位_索引V += 1

                        self.更新标签F(i)
                        i += 1
                        print(11111111111111111111)

                    # 修改子标签的第四位_索引V
                    self.增加_四级_索引F(选定序号V)

                else:
                    ui.notify("修改标签等级F-提高等级：第三位位置已满，无法提升等级")

        self.更新标签F(选定序号V)

        pprint(f"""
**************************标签生成器C--修改标签等级F**********************
标注GL：{标注GL}
######################################
            """)

    def 标号重标注_减F(self, 目标等级VE: 等级E, 截至等级VE: 等级E):
        i = 当前标签G + 1
        while i < self._长度V:
            if 等级E.一 == self.标注VL[i].等级VE or self.标注VL[i].等级VE == 截至等级VE:
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

    def 增加_二级_索引F(self, 序号V: int):
        """当前标签之后的所有标签第二位索引+1，即向后移一位"""
        i = 序号V + 1
        while i < self._长度V:
            if 等级E.一 == self.标注VL[i].等级VE:
                break

            self.标注VL[i].第二位_索引V = self.标注VL[i - 1].第二位_索引V + 1
            self.更新标签F(i)
            i += 1

    def 增加_四级_索引F(self, 序号V: int):
        """四级标签的索引+1"""
        j = 序号V + 1
        while j < self._长度V:
            if 等级E.四 == self.标注VL[j].等级VE:
                self.标注VL[j].第四位_索引V = self.标注VL[j - 1].第四位_索引V + 1
                self.更新标签F(j)
            else:
                break

            j += 1

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

    def 添加标签F(self, 零件名V: str = "XXX"):
        """生成指定等级的标签组件"""

        global 标注GL, 第三方标记G
        第三方标记G = False

        if not self.是否_超出索引V:
            self.获取索引F()
            后缀V, 重名次数V = self.零件名_重名_后缀F(零件名V)

            # 如果在尾部添加新建新标签
            if self._长度V == 0 or self._长度V - 1 == 当前标签G:
                self.生成标签F(
                    等级G,
                    self.第一位_索引V,
                    self.第二位_索引V,
                    self.第三位_索引V,
                    self.第四位_索引V,
                    后缀V,
                    重名次数V,
                    零件名V,
                )

            # 在中间添加新建新标签
            else:
                序号V: int = self.获取_插入_序号F()

                self.标签O: 标签C = 标签C(
                    序号V=序号V,
                    等级V=等级G,
                    零件名VS=零件名V,
                    第一位_索引V=self.第一位_索引V,
                    第二位_索引V=self.第二位_索引V,
                    第三位_索引V=self.第三位_索引V,
                    第四位_索引V=self.第四位_索引V,
                    后缀V=后缀V,
                    重名次数V=重名次数V,
                )
                self.标签O.move(target_container=生成区域G, target_index=序号V)
                self.标注VL.insert(序号V, self.标签O)
                标注GL.insert(
                    序号V,
                    [
                        等级G,
                        self.第一位_索引V,
                        self.第二位_索引V,
                        self.第三位_索引V,
                        self.第四位_索引V,
                        零件名V,
                        后缀V,
                        重名次数V,
                        self.标签O.文本V,
                    ],
                )

                self._长度V += 1

                # 更改后续标签对象的序号
                i = 序号V + 1
                while i < self._长度V:
                    self.标注VL[i].序号V += 1
                    i += 1

                # 更改后续标签的标号
                if 等级E.一 == 等级G:
                    self.修改第一位索引F(序号V, True)
                elif 等级E.二 == 等级G:
                    self.标号重标注_加F(序号V, 等级E.二, 等级E.一)
                elif 等级E.三 == 等级G:
                    self.标号重标注_加F(序号V, 等级E.三, 等级E.二)
                elif 等级E.四 == 等级G:
                    self.标号重标注_加F(序号V, 等级E.四, 等级E.三)

                # 修改后缀，后边的标签可能与新加的重名，所以需要修改
                self.新增是否重复F(序号V, 零件名V)

            self.标签O.是否_checkbox_选中 = True  # 选中新生成的标签，并切换当前标签G
            pprint(f"""
                *****************************添加标签F-标注G********************************
                长度：【{self._长度V}】个元素；
                标注GL：{标注GL}
                ####################################
                """)
            print(
                "++++++++++++++++++++++++++++++++++++++++++++++添加标签结束++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            )

    def 生成标签F(
        self,
        等级VE: 等级E,
        第一位_索引V: int,
        第二位_索引V: int,
        第三位_索引V: int,
        第四位_索引V: int,
        后缀V: str,
        重名次数V: int,
        零件名V: str,
    ):
        global 标注GL

        self.标签O: 标签C = 标签C(
            序号V=self._长度V,
            等级V=等级VE,
            零件名VS=零件名V,
            第一位_索引V=第一位_索引V,
            第二位_索引V=第二位_索引V,
            第三位_索引V=第三位_索引V,
            第四位_索引V=第四位_索引V,
            后缀V=后缀V,
            重名次数V=重名次数V,
        )

        self.标签O.move(target_container=生成区域G, target_index=self._长度V)
        self.标注VL.append(self.标签O)
        标注GL.append(
            [
                等级G,
                self.第一位_索引V,
                self.第二位_索引V,
                self.第三位_索引V,
                self.第四位_索引V,
                零件名V,
                后缀V,
                重名次数V,
                self.标签O.文本V,
            ]
        )

        self._长度V += 1

    def 获取_插入_序号F(self) -> int:
        """假设当前标签的等级是一级，那么在中间插入标签，
        新插入的标签应该也是一级，所以要跳过其他相邻的但等级不是一的标签
        """
        序号V: int = 0
        if 等级E.一 == 等级G:
            序号V = self.筛选索引F(等级E.一)
        elif 等级E.二 == 等级G:
            序号V = self.筛选索引F(等级E.二)
        elif 等级E.三 == 等级G:
            序号V = self.筛选索引F(等级E.三)
        elif 等级E.四 == 等级G:
            序号V = 当前标签G + 1

        return 序号V

    def 筛选索引F(self, 截至等级VE: 等级E) -> int:
        i = 当前标签G + 1
        while i < self._长度V:
            if self.标注VL[i].等级VE == 截至等级VE:
                return i
            i += 1

        return 当前标签G + 1

    def 修改第一位索引F(self, 序号V: int, 增加V: bool):
        """修改【序号V】后面所有标签的的第一位索引"""
        i = 序号V + 1
        while i < self._长度V:
            if 增加V:
                self.标注VL[i].第一位_索引V += 1
            else:
                self.标注VL[i].第一位_索引V -= 1

            self.更新标签F(i)

            i += 1

    def 标号重标注_加F(self, 序号V: int, 目标等级VE: 等级E, 截至等级VE: 等级E):
        i = 序号V + 1
        while i < self._长度V:
            if 等级E.一 == self.标注VL[i].等级VE or self.标注VL[i].等级VE == 截至等级VE:
                break  # 循环到截至等级的标签，就不需要在修改了
            else:
                if 等级E.二 == 目标等级VE:
                    self.标注VL[i].第二位_索引V += 1
                elif 等级E.三 == 目标等级VE:
                    self.标注VL[i].第三位_索引V += 1
                elif 等级E.四 == 目标等级VE:
                    self.标注VL[i].第四位_索引V += 1

                self.更新标签F(i)
            i += 1

    async def 重输_零件名F(self):
        输入V = await 输入框C()
        if 输入V:
            self.修改零件名F(当前标签G, 输入V)

    def 新增是否重复F(self, 序号V: int, 新增零件名V: str):
        i = 序号V + 1
        while i < self._长度V:
            if 新增零件名V == self.标注VL[i].零件名V:
                self.标注VL[i].重名次数V += 1
                self.标注VL[i].后缀V = 后缀_默认GL[self.标注VL[i].重名次数V]
                self.更新标签F(i)
            i += 1

    def 修改零件名F(self, 序号V: int, 输入V: str):
        后缀V, 重名次数V = self.零件名_重名_后缀F(输入V)
        self.标注VL[序号V].零件名V = 输入V
        self.标注VL[序号V].后缀V = 后缀V
        self.标注VL[序号V].重名次数V = 重名次数V
        self.更新标签F(序号V)

    def 更新标签F(self, 序号V: int):
        global 标注GL
        self.标注VL[序号V].刷新标签F()

        item: dict = [
            self.标注VL[序号V].等级VE,
            self.标注VL[序号V].第一位_索引V,
            self.标注VL[序号V].第二位_索引V,
            self.标注VL[序号V].第三位_索引V,
            self.标注VL[序号V].第四位_索引V,
            self.标注VL[序号V].零件名V,
            self.标注VL[序号V].后缀V,
            self.标注VL[序号V].重名次数V,
            self.标注VL[序号V].文本V,
        ]

        标注GL[序号V] = item

    def 零件名_重名_后缀F(self, 零件名V):
        result: int = 0

        if self._长度V > 0:
            i: int = 0
            while i <= 当前标签G:
                if self.标注VL[i].零件名V == 零件名V:
                    result += 1
                    print(
                        f"标签生成器C--零件名_重名_后缀F: 标注VL[i].零件名V->{self.标注VL[i].零件名V}；零件名V->{零件名V}；result->{result}；i->{i}"
                    )
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
                    # 当第一位索引加到头后，自动切换等级
                    等级G = 等级E.二
                    self.获取索引F()
                    ui.notify("""
                        第一位已到极限！请妥善安排命名结构！
                        源自：标签生成器C.索引递增F
                        """)
            elif 等级E.二 == 等级G:
                if self.计数F(等级E.二, 等级E.一) < self.第二位_长度V:
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
                if self.计数F(等级E.三, 等级E.二) < self.第三位_长度V:
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
                if self.计数F(等级E.四, 等级E.三) < self.第四位_长度V:
                    self.第一位_索引V = self.标注VL[当前标签G].第一位_索引V
                    self.第二位_索引V = self.标注VL[当前标签G].第二位_索引V
                    self.第三位_索引V = self.标注VL[当前标签G].第三位_索引V
                    self.第四位_索引V = self.标注VL[当前标签G].第四位_索引V + 1
                else:
                    self.是否_超出索引V = True
                    ui.notify("""
                        第四位已到极限！请妥善安排命名结构！
                        源自：标签生成器C.索引递增F
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
