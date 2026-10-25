"""Create sofa leg stoppers."""
from dataclasses import dataclass
from typing import Callable

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

@dataclass
class Boundry:
    """Create the boundry of the sheet"""
    width: float
    height: float

    def __call__(self):
        return [
            Draft.make_rectangle(self.width, self.height),
        ]


@dataclass
class Stopper:
    """Create a stopper"""
    bottom_width: float
    top_width: float
    height: float
    hole_radius: float

    def __call__(self):
        return [
          # Stopper base
          Draft.make_wire(
            [
              App.Vector(-self.bottom_width / 2, 0, 0),
              App.Vector(-self.top_width / 2, self.height, 0),
              App.Vector(self.top_width / 2, self.height, 0),
              App.Vector(self.bottom_width / 2, 0, 0),
            ],
            closed=True,
          ),
          # Stopper whole
          Draft.make_circle(
            self.hole_radius,
            placement=App.Placement(
              App.Vector(0, self.height, 0),
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

@dataclass
class Move:
    """Move the shap with the given vector."""
    shape: Callable[[], object]
    by: App.Vector

    def __call__(self)-> object:
        return Draft.move(self.shape(), self.by, copy=False)
        
        
def main():
    """Entry point to the program."""
    doc = App.newDocument()
    export_list = [ to_object(doc, repr(f), f())
      for (padding, bottom_width, top_width, height, hole_radius) in [
          (cm(.5), cm(12), cm(4), cm(12), cm(1)),
      ]
      for f in [
          Boundry(
              width=cm(25.5),
              height=cm(25.5),
          ),
          # Long Stoppers
          *[Move(
              shape=Rotate(
                shape=Stopper(
                  bottom_width=bottom_width,
                  top_width=top_width,
                  height=height,
                  hole_radius=hole_radius,
                ),
                angle=angle,
                center=App.Vector(0, 0, 0),
                axis=App.Vector(0, 0, 1),
              ),
              by=by,
              ) for (angle, by) in [
                    (0, App.Vector(
                          0.5 * bottom_width + padding,
                          padding,
                          0,
                        )
                    ),
                    (0, App.Vector(
                          1 * bottom_width + 2 * padding + 0.5 * top_width,
                          2 * padding + height,
                          0,
                        )
                    ),
                    (180, App.Vector(
                          0.5 * bottom_width + padding,
                          2 * padding + height * 2,
                          0,
                        )
                    ),
                ]
          ]
      ]
    ]
    doc.recompute()
    importSVG.export(export_list, './leg-stopper.svg')

if __name__ == "__main__":
    main()
