from panda3d.core import NodePath, Vec3
from primitive.polygon import Polygon, Cube, Plane
from primitive.render import RenderEntity
from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText

class App(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()

        # 床
        floor = RenderEntity(self.render, "floor")
        floor.set_polygon(Plane(size=5.0))
        floor.set_pos(0, 0, 0.0)
        

        # 空のエンティティ作成
        self.entity = RenderEntity(self.render, "cube_entity")

        # キューブの形状を作成
        cube = Cube(size=0.2)
        # 形状注入
        self.entity.set_polygon(cube)

        # Cubeの位置はそのまま
        self.entity.set_pos(0, 1.5, 0.2)

        # カメラの位置設定
        self.cam.setPos(0, 0.0, 0.5)
        self.cam.lookAt(self.entity.np)

        # テキスト（右下）
        self.pos_text = OnscreenText(
            text="", pos=(1.2, -0.95),  # 右下
            scale=0.05, fg=(1, 1, 1, 1), align=TextNode.ARight, mayChange=True
        )
        self.taskMgr.add(self.update_text, "update_text_task")

        # 入力（1回で1cm）
        self.step = 0.01
        self.step_deg = 5  # 5度
        self.accept("j", self.entity.move, [-self.step, 0, 0])  # 左へ
        self.accept("k", self.entity.move, [ self.step, 0, 0])  # 右へ
        self.accept("i", self.entity.move, [0, self.step, 0])  # 前へ
        self.accept("m", self.entity.move, [0, -self.step, 0])  # 後ろへ
        self.accept("w", self.entity.move, [0, 0, self.step])  # 上へ
        self.accept("s", self.entity.move, [0, 0, -self.step])  # 下へ
        self.accept("f", self.entity.rotate, [0, 0, self.step_deg])  # 右回転
        self.accept("a", self.entity.rotate, [0, 0, -self.step_deg])  # 左回転
        self.accept("r", self.entity.rotate, [self.step_deg, 0, 0])  # 上回転
        self.accept("v", self.entity.rotate, [-self.step_deg, 0, 0])  # 下回転
        self.accept("t", self.entity.rotate, [0, self.step_deg, 0])  # 時計回り
        self.accept("g", self.entity.rotate, [0, -self.step_deg, 0])  # 反時計回り
        self.accept("escape", self.userExit)


    def update_text(self, task):
        pos = self.entity.np.getPos(self.render)
        self.pos_text.setText(f"x={pos.x:.2f}  y={pos.y:.2f}  z={pos.z:.2f}")
        return task.cont

if __name__ == "__main__":
    App().run()