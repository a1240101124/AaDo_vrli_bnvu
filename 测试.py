from pprint import pprint

import 读写M
from nicegui import ui
from 配置M import 常量_路径

# 配置O = 读写M.配置C()
# 配置O.读取配置F()
# 配置O.写入配置F(0, 0, 0, 1, 0, 0)
# 配置O.读取配置F()
# 配置O.写入配置F()
# 配置O.读取配置F()
# data = [[4, "1", "1", "1", "a", "支杆", "一"], [4, "1", "1", "1", "a", "等级", "一"]]
# pprint(常量_路径)
# 项目O = 读写M.项目C(常量_路径)
# 项目O.保存F(data)
# 项目O.读取F()

# with (
#     ui.left_drawer(value=True).classes("bg-blue-grey-1").style("width: 300px!important;") as left_drawer
# ):  # props可以调整宽度，style不行
#     ui.button(text="123").props("flat").classes("text-blue-grey-10")

toggle1 = ui.toggle([1, 2, 3], value=1)
pprint(type(toggle1.value))

ui.run()
