from geant4_pybind import *

class EventAction(G4UserEventAction):

  def __init__(self):
    super().__init__()


  def EndOfEventAction(self, evt):
    pass
