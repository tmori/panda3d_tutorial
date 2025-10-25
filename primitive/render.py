from panda3d.core import NodePath, Vec3
from primitive.polygon import Polygon

class RenderEntity:
    """NodePath を持ち、Polygon から受け取った GeomNode をぶら下げる"""
    def __init__(self, parent, name: str = "entity"):
        self.np = parent.attachNewNode(name)
        self._geom_np = None  # 子ジオメトリの NodePath

    def set_polygon(self, poly: Polygon):
        node = poly.make_geom_node()
        # 既存を差し替え
        if self._geom_np is not None:
            self._geom_np.removeNode()
        self._geom_np = self.np.attachNewNode(node)
        # 裏面が消えるのが気になるなら TwoSided
        self._geom_np.setTwoSided(False) #裏面は描画しない

    # 位置・姿勢などの薄いAPI（必要に応じて）
    def set_pos(self, x, y, z): 
        self.np.setPos(x, y, z)

    def move(self, dx=0, dy=0, dz=0): 
        self.np.setPos(self.np.getPos() + Vec3(dx, dy, dz))

    def set_hpr(self, h, p, r): 
        self.np.setHpr(h, p, r)

    def rotate(self, dh=0, dp=0, dr=0): 
        h, p, r = self.np.getHpr()
        self.np.setHpr(h + dh, p + dp, r + dr)
