from pprint import pprint

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
from nicegui import ui

import 读写M
from 配置M import 常量_路径

with (
    ui.left_drawer(value=True).classes("bg-blue-grey-1").style("width: 300px!important;") as left_drawer
):  # props可以调整宽度，style不行
    ui.button(text="123").props("flat").classes("text-blue-grey-10")


ui.run()
