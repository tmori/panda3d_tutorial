from abc import ABC, abstractmethod
from typing import List, Tuple
from panda3d.core import (
    GeomNode, Geom, GeomVertexData, GeomVertexFormat, GeomVertexWriter,
    GeomTriangles, Vec3
)
Color = Tuple[float, float, float, float]

class Polygon(ABC):
    """形状の抽象：GeomNode を作って返す責務だけを持つ"""
    @abstractmethod
    def make_geom_node(self, name: str = "poly") -> GeomNode:
        pass

class Cube(Polygon):
    def __init__(self, size: float = 0.2, vertex_colors: List[Color] | None = None):
        self.size = size
        s = size * 0.5
        # 8頂点
        self.vtx: List[Vec3] = [
            Vec3(-s, -s, -s), Vec3( s, -s, -s), Vec3( s,  s, -s), Vec3(-s,  s, -s),
            Vec3(-s, -s,  s), Vec3( s, -s,  s), Vec3( s,  s,  s), Vec3(-s,  s,  s),
        ]
        # 12三角形（6面×2）
        self.tris: List[Tuple[int,int,int]] = [
            (0,1,2), (0,2,3),     # -Z
            (4,6,5), (4,7,6),     # +Z
            (1,5,6), (1,6,2),     # +X
            (0,3,7), (0,7,4),     # -X
            (3,2,6), (3,6,7),     # +Y
            (0,4,5), (0,5,1),     # -Y
        ]
        if vertex_colors is None:
            self.colors: List[Color] = [
                (1,0,0,1),(0,1,0,1),(0,0,1,1),(1,1,0,1),
                (1,0,1,1),(0,1,1,1),(1,1,1,1),(0.5,0.5,0.5,1),
            ]
        else:
            assert len(vertex_colors) == 8
            self.colors = vertex_colors

    def make_geom_node(self, name: str = "cube") -> GeomNode:
        vformat = GeomVertexFormat.getV3c4()  # 位置＋頂点色（最小構成）
        vdata = GeomVertexData(name, vformat, Geom.UH_static)
        vdata.setNumRows(len(self.vtx))

        vw = GeomVertexWriter(vdata, "vertex")
        cw = GeomVertexWriter(vdata, "color")
        for p, col in zip(self.vtx, self.colors):
            vw.addData3f(p)
            cw.addData4f(*col)

        prim = GeomTriangles(Geom.UH_static)
        for a, b, c in self.tris:
            prim.addVertices(a, b, c)
        prim.closePrimitive()

        geom = Geom(vdata); geom.addPrimitive(prim)
        node = GeomNode(name); node.addGeom(geom)
        return node