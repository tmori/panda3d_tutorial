from panda3d.core import NodePath, Vec3
from primitive.polygon import Polygon, Cube
from primitive.render import RenderEntity
from direct.showbase.ShowBase import ShowBase

class App(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()

        # 空のエンティティ作成
        self.entity = RenderEntity(self.render, "cube_entity")

        # キューブの形状を作成
        cube = Cube(size=0.2)
        # 形状注入
        self.entity.set_polygon(cube)

        # エンティティの位置設定
        self.entity.set_pos(0, 1.5, 0.2)

        # カメラの位置設定
        self.cam.setPos(0, 0.5, 0.5)
        self.cam.lookAt(self.entity.np)

        # 入力（1回で1cm）
        self.step = 0.01
        self.accept("j", self.entity.move, [ self.step, 0, 0])  # 右へ
        self.accept("k", self.entity.move, [-self.step, 0, 0])  # 左へ
        self.accept("escape", self.userExit)

if __name__ == "__main__":
    App().run()