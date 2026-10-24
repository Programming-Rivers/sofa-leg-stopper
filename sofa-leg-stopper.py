import FreeCAD as App
import Draft
import importSVG

doc = App.newDocument()

stopper_base = Draft.make_rectangle(10, 10)

stopper = doc.addObject("App::DocumentObjectGroup", "stopper")
stopper.Group = [
  stopper_base,
]

export_list = [
  stopper,
]
doc.recompute()
importSVG.export(export_list, './leg-stopper.svg')
print('You are running a FreeCAD script.')