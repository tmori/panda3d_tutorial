from panda3d.core import NodePath, Vec3, Point3
from primitive.polygon import Polygon, Cube, Plane
from primitive.render import RenderEntity
from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from core.camera import OrbitCamera 
from core.light import LightRig
import panda3d
print(f"--- Running Panda3D Version: {panda3d.__version__} ---")

class App(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()

        self.render.setShaderAuto()

        drone_model = RenderEntity(self.render, "drone_model")
        drone_model.load_model(self.loader, "assets/models/dji_avatar2.glb", copy=False)
        drone_model.set_pos(0, 0.0, 1)
        drone_model._geom_np.setHpr(0, 180, 0)

        # --- 照明セットアップ（先に設定） ---
        self.lights = LightRig(self.render, shadows=True)

        # 床
        floor = RenderEntity(self.render, "floor")
        floor.set_polygon(Plane(size=5.0))
        floor.set_pos(0, 0, 0.0)
        #floor.np.set_tag('ShadowReceiver', 'true')

        # 床は影を受ける
        floor.np.show()  # 念のため

        # 空のエンティティ作成
        self.entity = drone_model


        self.entity.np.set_tag('ShadowCaster', 'true')


        # --- ここからカメラ ---
        target = Point3(drone_model.np.getPos(self.render))
        self.cam_ctrl = OrbitCamera(
            self,
            target=target,
            distance=2.0,
            yaw_deg=35.0,
            pitch_deg=30.0
        )
        self.cam_ctrl.enable()

        # キーバインド
        self.accept("1", lambda: self.lights.toggle(True))
        self.accept("2", lambda: self.lights.toggle(False))

        # テキスト（右下）
        self.pos_text = OnscreenText(
            text="", pos=(1.2, -0.95),
            scale=0.05, fg=(1, 1, 1, 1), align=TextNode.ARight, mayChange=True
        )
        self.taskMgr.add(self.update_text, "update_text_task")

        # 入力（1回で1cm）
        self.step = 0.01
        self.step_deg = 5
        self.accept("j", self.entity.move, [-self.step, 0, 0])
        self.accept("k", self.entity.move, [ self.step, 0, 0])
        self.accept("i", self.entity.move, [0, self.step, 0])
        self.accept("m", self.entity.move, [0, -self.step, 0])
        self.accept("w", self.entity.move, [0, 0, self.step])
        self.accept("s", self.entity.move, [0, 0, -self.step])
        self.accept("f", self.entity.rotate, [0, 0, self.step_deg])
        self.accept("a", self.entity.rotate, [0, 0, -self.step_deg])
        self.accept("r", self.entity.rotate, [self.step_deg, 0, 0])
        self.accept("v", self.entity.rotate, [-self.step_deg, 0, 0])
        self.accept("t", self.entity.rotate, [0, self.step_deg, 0])
        self.accept("g", self.entity.rotate, [0, -self.step_deg, 0])
        self.accept("escape", self.userExit)

    def update_text(self, task):
        pos = self.entity.np.getPos(self.render)
        self.pos_text.setText(f"x={pos.x:.2f}  y={pos.y:.2f}  z={pos.z:.2f}")
        return task.cont

if __name__ == "__main__":
    App().run()