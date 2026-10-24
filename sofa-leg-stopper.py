"""Create sofa leg stoppers."""
from dataclasses import dataclass

import FreeCAD as App
import Draft
import importSVG

def cm(v: float) -> float:
    """Converts mm to cm."""
    return v * 10


def to_object(doc, name: str, objects: list):
    """Create an object from the given name and list of objects."""
    obj = doc.addObject("App::DocumentObjectGroup", name)
    obj.Group = objects
    return obj


def boundry():
    """Create the boundry of the sheet"""
    return [
        Draft.make_rectangle(cm(25.5), cm(25.5)),
    ]


@dataclass
class Stopper:
    """Create a stopper"""
    x: float   # middle
    y: float   # bottom
    bottom_width: float
    top_width: float
    height: float
    hole_radius: float

    def __call__(self):
        return [
          # Stopper base
          Draft.make_wire(
            [
              App.Vector(self.x - self.bottom_width / 2, self.y, 0),
              App.Vector(self.x - self.top_width / 2, self.height, 0),
              App.Vector(self.x + self.top_width / 2, self.height, 0),
              App.Vector(self.x + self.bottom_width / 2, self.y, 0),
            ],
            closed=True,
          ),
          # Stopper whole
          Draft.make_circle(
            self.hole_radius,
            placement=App.Placement(
              App.Vector(self.x, self.y + self.height, 0),
              App.Rotation(0, 0, 1)),
              startangle=180,
              endangle=0,
          ),
        ]


@dataclass
class Rotate:
    """Rotates the shape around the given center by the given angle amount."""
    shape: Callable[[], object]
    angle: float
    center: App.Vector
    axis: App.Vector

    def __call__(self):
        return Draft.rotate(self.shape(), self.angle, self.center)

def main():
    """Entry point to the program."""
    doc = App.newDocument()
    export_list = [ to_object(doc, str(f), f())
      for (padding, bottom_width, top_width, height, hole_radius) in [
          (cm(6.1), cm(12), cm(4), cm(12), cm(1)),
      ]
      for f in [
          boundry,
          *[Rotate(
                shape=Stopper(
                  x=padding + bottom_width / 2 * 3 * i,
                  y=cm(0),
                  bottom_width=bottom_width,
                  top_width=top_width,
                  height=height,
                  hole_radius=hole_radius,
                ),
                angle=angle,
                center=App.Vector(padding + bottom_width / 2 * 3 * i, height* 1.01, cm(0)),
                axis=App.Vector(0, 0, 1),
          ) for i in range (4) for angle in (0, 180)],
      ]
    ]
    doc.recompute()
    importSVG.export(export_list, './leg-stopper.svg')

if __name__ == "__main__":
    main()
