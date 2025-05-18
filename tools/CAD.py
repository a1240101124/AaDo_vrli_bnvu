r"""
创建者: 阿斗是只猫
创建日期: 2025-05-13
最后编辑人: 阿斗是只猫
最后编辑时间: 2025-05-17
说明:

    如有问题或建议，请联系微信公众号：【阿斗的小窝】

    Copyright (c) 2025 by 阿斗是只猫, All Rights Reserved.
"""

import re
from math import cos, radians, sin
from time import sleep

import pyautocad
import pythoncom
import win32com.client
from nicegui import ui
from pyautocad import APoint


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# 🔵                           共用方法                          🔵
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# region 🔛
def vtpnt(x, y, z=0):
    """坐标点转化为浮点数数组变体"""
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x, y, z))


def vtFloat(values: list):
    """列表转化为浮点数数组变体"""
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, values)


# endregion 🔚


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# 🔵                           CAD类                          🔵
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# region 🔛
class CADLabelManager:
    _instance = None  # 类属性，用于存储单例实例

    def __new__(cls):
        """重写 __new__ 方法，确保类只有一个实例"""
        if cls._instance is None:
            # 如果实例尚未创建，调用父类的 __new__ 方法创建一个新的实例
            cls._instance = super().__new__(cls)
            # 初始化实例
            cls._instance.__init__()
        # 返回已创建的实例
        return cls._instance

    def __init__(self):
        # 确保初始化逻辑只执行一次
        if not hasattr(self, "initialized"):
            self.acad = None
            self.doc = None
            self.app = None
            self.label_layer = "AutoLabel_Layer"
            self.插入点_调整系数: float = 0.5
            self.label_color_index = 141  # 索引颜色
            self.connect_cad()
            self.initialized = True  # 标记已初始化

    def connect_cad(self):
        """建立与AutoCAD的COM连接"""
        try:
            self.acad = pyautocad.Autocad(create_if_not_exists=True)
            self.doc = self.acad.ActiveDocument
            self.app = self.doc.Application
            print(f"成功连接到AutoCAD版本：{self.acad.app.Version}")
        except pythoncom.com_error as e:
            print(f"连接失败：{e!s}")
            raise

    def parse_labels(self, label_str):
        """改进的标签解析方法"""
        label_map = {}
        entries = re.split(r"[;\uff1b]", label_str)  # 匹配中英文分号
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            match = re.match(r"([^、,]+)[、,]\s*([^、,]+)", entry)
            if match:
                num = match.group(1).strip()
                text = match.group(2).strip()
                label_map[num] = text
                print(f"DEBUG - 解析到标签: {num} => {text}")  # 调试输出
        return label_map

    def create_layer(self):
        """创建或获取标签图层，并确保其状态正常"""
        layers = self.doc.Layers

        try:
            # 尝试创建图层
            layer = layers.Add(self.label_layer)
            print(f"创建新图层: {self.label_layer}")
        except pythoncom.com_error as e:
            if "重名" in str(e).lower():
                # 图层已存在，获取图层
                layer = layers.Item(self.label_layer)
                print(f"使用现有图层: {self.label_layer}")

                # 检查并修复图层状态
                if not layer.LayerOn:
                    print(f"图层 {self.label_layer} 被关闭，现在打开")
                    layer.LayerOn = True

                if layer.Freeze:
                    print(f"图层 {self.label_layer} 被冻结，现在解冻")
                    layer.Freeze = False
            else:
                raise

        # 设置图层颜色
        layer.color = self.label_color_index

        # 确保图层可写
        if layer.Lock:
            print(f"图层 {self.label_layer} 被锁定，现在解锁")
            layer.Lock = False

        # 临时切换到其他图层，避免操作当前图层时出错
        original_layer = self.doc.ActiveLayer.Name
        if original_layer == self.label_layer:
            try:
                # 尝试切换到0图层
                zero_layer = layers.Item("0")
                self.doc.ActiveLayer = zero_layer
                print(f"已从图层 {self.label_layer} 切换到图层 0")
            except Exception as e:
                # 如果0图层不存在或有问题，尝试创建一个临时图层
                temp_layer_name = "TempLayerForLabeling"
                try:
                    temp_layer = layers.Add(temp_layer_name)
                    self.doc.ActiveLayer = temp_layer
                    print(f"已从图层 {self.label_layer} 切换到临时图层 {temp_layer_name}")
                except Exception as e:
                    print(f"无法切换图层: {e!s}")
                    # 尝试重新获取图层并继续
                    layer = self.create_layer()

        return layer

    def calculate_adaptive_offset(self, original_text, text_to_add, height):
        """计算自适应的偏移量，考虑文本长度和复杂度"""
        # 基础偏移量 - 略微减小基础值
        base_offset = height * 1.8

        # 考虑原始文本长度的调整 - 减小调整因子，使调整更平缓
        original_length_factor = 1 + len(original_text) * 0.03

        # 考虑目标文本长度的调整 - 进一步减小调整因子
        target_length_factor = 1 + len(text_to_add) * 0.02

        # 特殊字符调整 - 区分字母和其他字符
        if re.search(r"[a-zA-Z]", original_text):
            special_char_factor = 0.65  # 包含字母的文本增加较小的偏移
        elif re.search(r"[^0-9]", original_text):  # 包含非数字字符
            special_char_factor = 0.7
        else:
            special_char_factor = 0.6  # 纯数字文本不增加额外偏移

        # 对较长文本的衰减调整 - 避免过长文本间隔过大
        length_damping = min(1.0 + len(original_text) * 0.01, 1.15)

        # 计算最终偏移量
        final_offset = (
            base_offset * original_length_factor * target_length_factor * special_char_factor / length_damping
        )
        return final_offset

    # def add_labels(self, label_str):
    #     """添加标签到当前图纸（支持单行/多行文字）"""
    #     label_map = self.parse_labels(label_str)
    #     layer = self.create_layer()

    #     model_space = self.doc.ModelSpace
    #     counter = 0

    #     for obj in self.acad.iter_objects(["Text", "MText"]):
    #         if not obj or obj.ObjectName not in ["AcDbText", "AcDbMText"]:
    #             continue
    #         try:
    #             if obj.ObjectName == "AcDbText":
    #                 content = obj.TextString.strip()
    #             elif obj.ObjectName == "AcDbMText":
    #                 raw_content = obj.TextString
    #                 content = re.sub(r"\\.*?[;}]", "", raw_content)
    #                 content = content.replace("\\L", "").replace("\\P", "\n")
    #                 content = content.strip()

    #             print(f"DEBUG - 发现文字对象: {content}")

    #             if content in label_map:
    #                 insert_point = APoint(obj.InsertionPoint)
    #                 height = obj.Height
    #                 rotation = obj.Rotation

    #                 # 计算自适应偏移量
    #                 offset = self.calculate_adaptive_offset(content, label_map[content], height)

    #                 # 根据文本旋转角度调整偏移方向
    #                 rotation_rad = radians(rotation)
    #                 delta_x = offset * cos(rotation_rad)
    #                 delta_y = offset * sin(rotation_rad)

    #                 new_point = APoint(insert_point.x + delta_x, insert_point.y + delta_y)

    #                 # 检查图层状态
    #                 if layer and layer.LayerOn and not layer.Freeze:
    #                     try:
    #                         # 尝试添加文本
    #                         new_text = model_space.AddText(label_map[content], new_point, height)
    #                         new_text.Layer = layer.Name
    #                         new_text.rotation = rotation
    #                         new_text.Alignment = 0
    #                         new_text.Color = self.label_color_index
    #                         counter += 1
    #                         if counter % 10 == 0:
    #                             self.doc.Regen(0)
    #                             sleep(0.1)
    #                     except Exception as e:
    #                         print(f"添加文本时出错: {e!s}")
    #                         # 尝试重新获取图层并继续
    #                         layer = self.create_layer()
    #                 else:
    #                     print(f"图层 {self.label_layer} 状态异常，无法添加文本")
    #                     # 尝试修复图层状态
    #                     layer = self.create_layer()

    #         except Exception as e:
    #             print(f"处理对象时出错：{e!s}")
    #             continue

    #     print(f"成功添加 {counter} 个标签")
    #     self.doc.Regen(0)

    def add_labels(self, label_str):
        """添加标签到当前图纸（支持单行/多行文字和多重引线）"""
        label_map = self.parse_labels(label_str)
        layer = self.create_layer()

        model_space = self.doc.ModelSpace
        counter = 0

        # --------- 先收集所有需要处理的原有对象 ----------
        original_objs = []
        for obj in self.acad.iter_objects(["Text", "MText", "MLeader"]):
            # 跳过本标签图层上的对象（防止新插入的对象被再次处理）
            obj_layer = getattr(obj, "Layer", None)
            if obj_layer == self.label_layer:
                continue
            if obj and obj.ObjectName in ["AcDbText", "AcDbMText", "AcDbMLeader"]:
                original_objs.append(obj)

        # --------- 处理收集到的对象 ----------
        for obj in original_objs:
            try:
                if obj.ObjectName == "AcDbText":  # noqa: SIM114
                    content = obj.TextString.strip()
                    insert_point = APoint(obj.InsertionPoint)
                    height = obj.Height
                    rotation = obj.Rotation
                elif obj.ObjectName == "AcDbMText":
                    content = obj.TextString.strip()
                    insert_point = APoint(obj.InsertionPoint)
                    height = obj.Height
                    rotation = obj.Rotation
                elif obj.ObjectName == "AcDbMLeader":
                    content = getattr(obj, "TextString", "").strip()
                    if not content:
                        print("多重引线没有注释内容，跳过")
                        continue

                    try:
                        vertices = obj.GetLeaderLineVertices(0)
                        if len(vertices) >= 3:
                            last_idx = len(vertices) - 3
                            kink_point = APoint(vertices[last_idx], vertices[last_idx + 1])
                        else:
                            print("多重引线点集不足，无法确定拐点，跳过")
                            continue
                    except Exception as e:
                        print("无法获取多重引线拐点:", e)
                        continue

                    height = getattr(obj, "TextHeight", 2.5)
                    rotation = getattr(obj, "TextRotation", 0)
                    insert_point = APoint(kink_point.x, kink_point.y - height * 0.55)

                print(f"DEBUG - 发现对象: {content} ({obj.ObjectName})")

                if content in label_map:
                    offset = self.calculate_adaptive_offset(content, label_map[content], height)
                    rotation_rad = radians(rotation)
                    delta_x = offset * cos(rotation_rad)
                    delta_y = offset * sin(rotation_rad)
                    # 插入点坐标
                    new_point = APoint(insert_point.x + delta_x, insert_point.y + delta_y)

                    if layer and layer.LayerOn and not layer.Freeze:
                        try:
                            # new_text = model_space.AddText(label_map[content], new_point, height)
                            # new_text.Layer = layer.Name
                            # new_text.rotation = rotation
                            # new_text.Alignment = 0  # 对其方式，左下（acAlignmentLeft）
                            # new_text.Color = self.label_color_index
                            self.创建_多重引线(layer, label_map[content], new_point, height)
                            counter += 1
                            if counter % 10 == 0:
                                self.doc.Regen(0)
                                sleep(0.1)
                        except Exception as e:
                            print(f"添加文本时出错: {e!s}")
                            layer = self.create_layer()
                    else:
                        print(f"图层 {self.label_layer} 状态异常，无法添加文本")
                        layer = self.create_layer()

            except Exception as e:
                print(f"处理对象时出错：{e!s}")
                continue

        print(f"成功添加 {counter} 个标签")
        self.doc.Regen(0)

    def 创建_多重引线(self, layer, 文本V: str, 插入点V: APoint, 字高V: float):
        try:
            start_point = APoint(插入点V.x, 插入点V.y + 字高V * self.插入点_调整系数)  # 引线起点（原对象的插入点）
            end_point = APoint(插入点V.x + 字高V, 插入点V.y + 3 * 字高V)  # 引线终点（偏移后的位置）

            # 构建符合COM接口要求的点数组
            leader_points = [
                float(start_point.x),
                float(start_point.y),
                0.0,
                float(end_point.x),
                float(end_point.y),
                0.0,
            ]

            # 使用pyautocad的aDouble方法转换点数组
            points_variant = self.acad.aDouble(leader_points)

            # 创建多重引线对象（使用AddMLeader方法）
            mleader = self.doc.ModelSpace.AddMLeader(points_variant, 0)

            # 设置基本属性
            mleader.Layer = layer.Name
            mleader.TextHeight = 字高V
            mleader.TextString = 文本V
            mleader.ArrowheadType = 1  # 箭头类型
            mleader.ArrowheadSize = 0.15  # 箭头高度

            # 刷新并应用设置
            mleader.Update()

        except pythoncom.com_error as e:
            # 增强COM错误处理
            if e.hresult == -2147418111:  # 被呼叫方拒绝接收呼叫
                print("COM错误: AutoCAD拒绝接收呼叫，尝试重新连接...")
                try:
                    self.connect_cad()
                    print("已重新连接到AutoCAD")
                    # 重试创建多重引线
                    return self.创建_多重引线(layer, 文本V, 插入点V, 字高V)
                except Exception as reconnect_e:
                    print(f"重新连接失败: {reconnect_e!s}")
            else:
                print(f"COM错误: {e.excepinfo[2] if e.excepinfo else str(e)}")
            raise
        except Exception as e:
            print(f"未知错误: {e!s}")
            raise

    def delete_labels_on_layer(self, layer_name):
        """删除指定图层上的所有文字对象（标签）"""
        try:
            # 检查图层是否存在
            layers = self.doc.Layers
            layer = layers.Item(layer_name)

            # 切换当前图层为目标图层
            # self.doc.ActiveLayer = layer

            # 确保图层是活动的且可写
            if not layer.LayerOn:
                print(f"图层 {layer_name} 被关闭，现在打开")
                layer.LayerOn = True

            if layer.Freeze:
                print(f"图层 {layer_name} 被冻结，现在解冻")
                layer.Freeze = False

            if layer.Lock:
                print(f"图层 {layer_name} 被锁定，现在解锁")
                layer.Lock = False

            # 获取模型空间
            model_space = self.doc.ModelSpace

            # # 收集所有文字对象
            # text_objects = []
            # for obj in self.acad.iter_objects("Text"):
            #     if obj.Layer == layer_name:
            #         text_objects.append(obj)
            # for obj in self.acad.iter_objects("MText"):
            #     if obj.Layer == layer_name:
            #         text_objects.append(obj)

            # 收集所有对象
            text_objects = []
            for obj in self.acad.iter_objects():
                if obj.Layer == layer_name:
                    text_objects.append(obj)

            print(f"找到 {len(text_objects)} 个文字对象需要删除")

            total_deleted = 0
            failed_objects = []

            for obj in text_objects:
                try:
                    # 检查对象是否被锁定或只读
                    if hasattr(obj, "Locked") and obj.Locked:
                        obj.Locked = False
                    if hasattr(obj, "ReadOnly") and obj.ReadOnly:
                        print(f"对象 {obj.ObjectName} 是只读的，无法删除")
                        continue

                    # 删除对象
                    obj.Delete()
                    total_deleted += 1
                except pythoncom.com_error as e:
                    print(f"删除对象 {obj.ObjectName} 时出错: {e!s}")
                    failed_objects.append(obj)

                # 增加延迟，避免并发问题
                sleep(0.1)

            # 尝试再次删除失败的对象
            if failed_objects:
                print(f"尝试重新删除 {len(failed_objects)} 个失败的对象")
                for obj in failed_objects:
                    try:
                        obj.Delete()
                        total_deleted += 1
                        print(f"重新删除成功: {obj.ObjectName}")
                    except pythoncom.com_error as e:
                        print(f"再次删除失败: {obj.ObjectName}, 错误: {e!s}")

            print(f"成功删除图层 {layer_name} 上的 {total_deleted} 个文字对象")
            self.doc.Regen(0)  # 刷新图形

        except pythoncom.com_error as e:
            if "无效名称" in str(e):
                print(f"图层 {layer_name} 不存在")
            elif "被呼叫方拒绝接收呼叫" in str(e):
                print(f"AutoCAD拒绝了删除操作，错误: {e!s}")
            else:
                print(f"处理图层 {layer_name} 时出错: {e!s}")

# endregion 🔚


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# 🔵                           供外部调用的接口                          🔵
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# region 🔛
def 标记F(label_str: str):
    """label_str = '100、支杆；110、支杆一；111、支杆二；111a、支杆三；200、支杆四；300、支杆五'"""
    label_mgr = None  # 显式初始化

    try:
        label_mgr = CADLabelManager()

        label_mgr.add_labels(label_str)

        # 检查 AutoCAD 是否处于正常状态
        if label_mgr.acad and label_mgr.doc:
            try:
                label_mgr.acad.prompt("CAD模块 操作已完成\n")
            except pythoncom.com_error as e:
                ui.notify(f"与AutoCAD交互时出错: {e!s}-01")
        else:
            ui.notify("CAD模块 未正确连接到AutoCAD实例-02")
    except Exception as e:
        ui.notify(f"CAD模块 操作失败：{e!s}-03")
    finally:
        # 安全访问检查
        if label_mgr and hasattr(label_mgr, "acad") and label_mgr.acad:
            try:
                label_mgr.acad.prompt("CAD模块 操作已完成-04\n")
            except pythoncom.com_error as e:
                ui.notify(f"与AutoCAD交互时出错: {e!s}-05")
        elif label_mgr:
            ui.notify("CAD连接未正确建立-06")
        else:
            ui.notify("CAD模块 程序初始化失败-07")


def 清空F():
    import contextlib

    label_mgr = None  # 显式初始化
    try:
        label_mgr = CADLabelManager()
        # 检查 AutoCAD 是否处于正常状态
        if label_mgr.acad and label_mgr.doc:
            try:
                label_mgr.acad.prompt("操作已完成\n")
            except pythoncom.com_error as e:
                ui.notify(f"与AutoCAD交互时出错: {e!s}-08")
        else:
            ui.notify("未正确连接到AutoCAD实例-09")

        # 测试删除图层上的标签
        label_mgr.delete_labels_on_layer(label_mgr.label_layer)

    except Exception as e:
        ui.notify(f"CAD模块 操作失败：{e!s}-10")
    finally:
        # 安全访问检查
        if label_mgr and hasattr(label_mgr, "acad"):
            with contextlib.suppress(Exception):
                label_mgr.acad.prompt("CAD模块 测试程序已退出\n")
        elif label_mgr:
            ui.notify("CAD连接未正确建立-11")
        else:
            ui.notify("CAD模块 程序初始化失败-12")

# endregion 🔚


# ------------- 测试 --------------
if __name__ in {"__main__", "__mp_main__"}:
    label_str = "100、支杆；110、支杆一；111、支杆二；111a、支杆三；200、支杆四；300、支杆五"
    label_mgr = None  # 显式初始化

    try:
        label_mgr = CADLabelManager()

        label_mgr.add_labels(label_str)

        # 检查 AutoCAD 是否处于正常状态
        if label_mgr.acad and label_mgr.doc:
            try:
                label_mgr.acad.prompt("CAD模块 操作已完成\n")
            except pythoncom.com_error as e:
                print(f"与AutoCAD交互时出错: {e!s}-01")
        else:
            print("CAD模块 未正确连接到AutoCAD实例-02")
    except Exception as e:
        print(f"CAD模块 操作失败：{e!s}-03")
    finally:
        # 安全访问检查
        if label_mgr and hasattr(label_mgr, "acad") and label_mgr.acad:
            try:
                label_mgr.acad.prompt("CAD模块 操作已完成-04\n")
            except pythoncom.com_error as e:
                print(f"与AutoCAD交互时出错: {e!s}-05")
        elif label_mgr:
            print("CAD连接未正确建立-06")
        else:
            print("CAD模块 程序初始化失败-07")
