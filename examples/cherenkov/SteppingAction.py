from geant4_pybind import *

class SteppingAction(G4UserSteppingAction):

  def __init__(self):
    super().__init__()

  def UserSteppingAction(self, aStep):
    pass
