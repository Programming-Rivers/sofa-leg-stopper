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
    long_width: float
    top_width: float
    height: float
    hole_radius: float

    def __call__(self):
        return [
          # Stopper base
          Draft.make_wire(
            [
              App.Vector(-self.long_width / 2, 0, 0),
              App.Vector(-self.top_width / 2, self.height, 0),
              App.Vector(self.top_width / 2, self.height, 0),
              App.Vector(self.long_width / 2, 0, 0),
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
    long_width, long_height = cm(12), cm(12)
    short_width, short_height = cm(9), cm(8)
    doc = App.newDocument()
    padding, top_width, hole_radius = cm(.5), cm(4), cm(1)

    export_list = [ to_object(doc, repr(f), f())
      for f in [
          Boundry(
              width=cm(25.5),
              height=cm(25.5),
          ),
          # Short Stopper
          Move(
              shape=Rotate(
                shape=Stopper(
                  long_width=short_width,
                  top_width=top_width,
                  height=short_height,
                  hole_radius=hole_radius,
                ),
                angle=180,
                center=App.Vector(0, 0, 0),
                axis=App.Vector(0, 0, 1),
              ),
              by=App.Vector(
                          2 * padding + long_width - top_width + 0.5 * short_width,
                          padding + long_height,
                          0,
                        )
          ),
          # Long Stoppers
          *[Move(
              shape=Rotate(
                shape=Stopper(
                  long_width=long_width,
                  top_width=top_width,
                  height=long_height,
                  hole_radius=hole_radius,
                ),
                angle=angle,
                center=App.Vector(0, 0, 0),
                axis=App.Vector(0, 0, 1),
              ),
              by=by,
              ) for (angle, by) in [
                    (0, App.Vector(
                          0.5 * long_width + padding,
                          padding,
                          0,
                        )
                    ),
                    (0, App.Vector(
                          1 * long_width + 2 * padding + 0.5 * top_width,
                          2 * padding + long_height,
                          0,
                        )
                    ),
                    (180, App.Vector(
                          0.5 * long_width + padding,
                          2 * padding + long_height * 2,
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
