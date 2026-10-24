import FreeCAD as App
import Draft
import importSVG

def cm(v: float) -> float:
  """Converts mm to cm."""
  return v * 10


def main():
  """Entry point to the program."""
  doc = App.newDocument()

  boundry_draft = Draft.make_rectangle(cm(25.5), cm(25.5))
  boundry = doc.addObject("App::DocumentObjectGroup", "boundry")
  boundry.Group = [
    boundry_draft,
  ]

  stopper_base = Draft.make_wire(
    [
      App.Vector(0, 0, 0),
      App.Vector(cm(4), cm(12.5), 0),
      App.Vector(cm(8), cm(12.5), 0),
      App.Vector(cm(12), cm(0), 0),
    ],
    closed=True,
  )
  stopper_tip = Draft.make_circle(
    cm(2),
    placement=App.Placement(
      App.Vector(cm(12) / 2, cm(12.5), 0),
      App.Rotation(0, 0, 1)),
    startangle=0,
    endangle=180,
  )
  stopper_whole = Draft.make_circle(
    cm(1),
    placement=App.Placement(
      App.Vector(cm(12) / 2, cm(11.5), 0),
      App.Rotation(0, 0, 1)),
  )

  stopper = doc.addObject("App::DocumentObjectGroup", "stopper")
  stopper.Group = [
    stopper_base,
    stopper_tip,
    stopper_whole,
  ]

  export_list = [
    boundry,
    stopper,
  ]
  doc.recompute()
  importSVG.export(export_list, './leg-stopper.svg')

if __name__ == "__main__":
  main()