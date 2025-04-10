r"""
创建者: 阿斗是只猫
创建日期: 2025-04-09
最后编辑人: 阿斗是只猫
最后编辑时间: 2025-04-09
说明:

    如有问题或建议，请联系微信公众号：【阿斗的小窝】

    Copyright (c) 2025 by 阿斗是只猫, All Rights Reserved.
"""

# 导入常用模块
from nicegui import ui


# 主函数
@ui.page(path="/")
async def _() -> None:
    pass


if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
