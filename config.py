r"""
创建者: 阿斗是只猫
创建日期: 2025-04-09
最后编辑人: 阿斗是只猫
最后编辑时间: 2025-04-10
说明:

    如有问题或建议，请联系微信公众号：【阿斗的小窝】

    Copyright (c) 2025 by 阿斗是只猫, All Rights Reserved.
"""

import sys
from pathlib import Path

####################################常量#############################################
常量_标题: str = "阿斗附图标记辅助 V1.0"
常量_路径 = None


####################################获取入口所在路径#############################################
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    # pyinstaller 打包的exe运行时，走这里
    常量_路径 = Path(sys.executable).parent
    常量_路径 = 常量_路径 / Path("_internal")
else:
    # 非 pyinstaller 执行
    常量_路径 = Path(__file__).parent.resolve()


####################################登录页面#############################################
