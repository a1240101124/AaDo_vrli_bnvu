from pyautocad import APoint

def 创建_多重引线(self, 文本V: str, 插入点V: APoint, 字高V: float):
        拐点V: APoint = APoint(插入点V.x + 字高V, 插入点V.y + 2 * 字高V)
        text = self.doc.ModelSpace.AddMText(拐点V, 字高V, 文本V)
        标注V: = 
        self.doc.ModelSpace.AddLeader()
