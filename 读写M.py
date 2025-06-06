r"""
创建者: 阿斗是只猫
创建日期: 2025-04-09
最后编辑人: 阿斗是只猫
最后编辑时间: 2025-04-13
说明:

    如有问题或建议，请联系微信公众号：【阿斗的小窝】

    Copyright (c) 2025 by 阿斗是只猫, All Rights Reserved.
"""

import sqlite3
from pathlib import Path

from 配置M import 常量_路径, 常量_项目名

###################################常量#############################################
常量_配置路径 = 常量_路径 / Path("static/配置.db")


####################################读取或更改配置#############################################
class 配置C:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(常量_配置路径)  # 创建或连接到数据库文件
        self.cu = self.conn.cursor()

    def 读取配置F(self):
        try:
            # 执行 SQL 查询语句，不选择 id 列，获取表中的第一行数据
            self.cu.execute(
                "SELECT 第二位_索引, 第三位_索引, 第四位_风格, 第四位_索引, 后缀_风格, 连接符_索引 FROM config LIMIT 1"
            )
            # 获取查询结果的第一行数据
            first_row = self.cu.fetchone()

            if first_row:
                print("配置内容：", first_row)
            else:
                print("表中没有数据。")
            return first_row
        except sqlite3.Error as e:
            print(f"发生错误: {e}")
            return (1, 1, 1, 0, 0, 0)

    def 写入配置F(
        self,
        第二位_索引: int = 1,
        第三位_索引: int = 1,
        第四位_风格: int = 1,
        第四位_索引: int = 0,
        后缀_风格: int = 0,
        连接符_索引: int = 0,
    ):
        try:
            # 使用 UPDATE 语句更新第一行数据
            query = """
            UPDATE config
            SET 第二位_索引 = ?, 第三位_索引 = ?, 第四位_风格 = ?,
                第四位_索引 = ?, 后缀_风格 = ?, 连接符_索引 = ?
            WHERE id = (SELECT MIN(id) FROM config);
            """
            values = (第二位_索引, 第三位_索引, 第四位_风格, 第四位_索引, 后缀_风格, 连接符_索引)
            self.conn.execute(query, values)
            self.conn.commit()
            print("配置已更新为：", values)
        except sqlite3.Error as e:
            print(f"发生错误: {e}")
            self.conn.rollback()


####################################项目：读取、保存#############################################
class 项目C:
    def __init__(self):
        pass

    def __初始化(self, 项目路径V):
        self.conn = sqlite3.connect(项目路径V)
        self.cu = self.conn.cursor()

        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS table1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "等级" INTEGER,
                "第一位索引" INTEGER,
                "第二位索引" INTEGER,
                "第三位索引" INTEGER,
                "第四位索引" INTEGER,
                "零件名" TEXT,
                "后缀" TEXT,
                "重名次数" INTEGER,
                "标签内容" TEXT
            )
            """
            self.cu.execute(create_table_query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"创建表时发生错误: {e}")
            self.conn.rollback()

    def 保存F(self, 项目路径V, data):
        temp = 项目路径V / Path(常量_项目名)
        self.__初始化(temp)

        # 例：data = [[4,1,1,1,"a","支杆","一",1,"111a、支杆一"],]
        try:
            # 清空旧数据
            self.conn.execute("DELETE FROM table1")
            # 插入数据
            insert_query = "INSERT INTO table1 (等级, 第一位索引, 第二位索引, 第三位索引, 第四位索引, 零件名, 后缀, 重名次数, 标签内容) VALUES (?,?,?,?,?,?,?,?,?)"
            for row in data:
                self.cu.execute(insert_query, row)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"保存数据时发生错误: {e}")
            self.conn.rollback()

    def 读取F(self, 项目路径V) -> list:
        result = []
        self.__初始化(项目路径V)

        try:
            # 不包含 id 列的查询
            select_query = "SELECT 等级, 第一位索引, 第二位索引, 第三位索引, 第四位索引, 零件名, 后缀, 重名次数, 标签内容 FROM table1 ORDER BY id"
            self.cu.execute(select_query)
            rows = self.cu.fetchall()
            result = [list(row) for row in rows]
            print("读取的数据：", result)
        except sqlite3.Error as e:
            print(f"读取数据时发生错误: {e}")
        return result

    def 关闭连接F(self):
        try:
            self.cu.close()
            self.conn.close()
        except sqlite3.Error as e:
            print(f"关闭数据库连接时发生错误: {e}")
