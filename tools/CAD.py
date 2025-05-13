r"""
创建者: 阿斗是只猫
创建日期: 2025-05-13
最后编辑人: 阿斗是只猫
最后编辑时间: 2025-05-13
说明:
    功能：
        对CAD文件进行操作，具体来说是向CAD写入或删除文本。

    如有问题或建议，请联系微信公众号：【阿斗的小窝】

    Copyright (c) 2025 by 阿斗是只猫, All Rights Reserved.
"""

import re
from time import sleep

import pyautocad
import pythoncom
from pyautocad import APoint


class CADLabelManager:
    def __init__(self):
        self.acad = None
        self.doc = None
        self.label_layer = "AutoLabel_Layer"
        self.label_color = (48, 132, 215)  # RGB颜色
        self.offset_factor = 2.0  # 增加偏移因子，避免重叠
        self.connect_cad()

    def connect_cad(self):
        """建立与AutoCAD的COM连接"""
        try:
            self.acad = pyautocad.Autocad(create_if_not_exists=True)
            self.doc = self.acad.ActiveDocument
            print(f"成功连接到AutoCAD版本：{self.acad.app.Version}")
        except pythoncom.com_error as e:
            print(f"连接失败：{e!s}")
            raise

    def parse_labels(self, label_str):
        """解析标注字符串"""
        label_map = {}
        entries = re.split(r"[；;]", label_str)
        for entry in entries:
            parts = re.split(r"[、,]", entry.strip())
            if len(parts) >= 2:
                num = parts[0].strip()
                text = parts[1].strip()
                label_map[num] = text
        return label_map

    def create_layer(self):
        """创建专用图层"""
        layers = self.doc.Layers
        try:
            layer = layers.Add(self.label_layer)
            # 只设置真彩色，移除旧的颜色索引设置
            layer.TrueColor.SetRGB(*self.label_color)
            print(f"已创建专用图层：{self.label_layer}")
        except pythoncom.com_error:
            layer = layers.Item(self.label_layer)
            # 确保现有图层使用正确的颜色
            layer.TrueColor.SetRGB(*self.label_color)
        return layer

    def add_labels(self, label_str):
        """添加标签到当前图纸"""
        label_map = self.parse_labels(label_str)
        layer = self.create_layer()

        model_space = self.doc.ModelSpace
        counter = 0

        # 遍历所有文字对象
        for text in self.acad.iter_objects("Text"):
            content = text.TextString.strip()
            if content in label_map:
                # 获取原始属性
                insert_point = APoint(text.InsertionPoint)
                height = text.Height
                rotation = text.Rotation

                # 计算新位置（根据文本高度和旋转角度动态调整偏移量）
                offset_distance = height * self.offset_factor

                # 根据旋转角度计算偏移后的新位置
                import math

                angle_rad = math.radians(rotation)
                new_x = insert_point.x + offset_distance * math.cos(angle_rad)
                new_y = insert_point.y + offset_distance * math.sin(angle_rad)
                new_point = APoint(new_x, new_y)

                # 创建新文字
                new_text = model_space.AddText(label_map[content], new_point, height)

                # 设置文字属性 - 只使用真彩色
                new_text.Layer = self.label_layer
                new_text.rotation = rotation
                new_text.TrueColor.SetRGB(*self.label_color)

                # 设置文字对齐方式，避免与原文本重叠
                new_text.Alignment = 1  # 左对齐（1=acAlignmentLeft）

                counter += 1
                if counter % 10 == 0:  # 分段提交防止COM超时
                    self.doc.Regen(0)
                    sleep(0.1)

        print(f"成功添加 {counter} 个标签")
        self.doc.Regen(0)

    def remove_labels(self):
        """移除所有自动添加的标签"""
        counter = 0
        for text in self.acad.iter_objects("Text"):
            if text.Layer == self.label_layer:
                text.Delete()
                counter += 1
                if counter % 10 == 0:
                    self.doc.Regen(0)
                    sleep(0.1)
        print(f"已移除 {counter} 个标签")
        self.doc.Regen(0)


# 使用示例
if __name__ == "__main__":
    try:
        label_mgr = CADLabelManager()

        # 标注字符串
        label_str = "100、支杆；110、支杆一；111、支杆二；111a、支杆三；200、支杆四；300、支杆五"

        # 添加标签
        label_mgr.add_labels(label_str)

        # 移除标签（演示用）
        # label_mgr.remove_labels()

    except Exception as e:
        print(f"操作失败：{e!s}")
    finally:
        if label_mgr.acad:
            label_mgr.acad.prompt("操作已完成\n")
