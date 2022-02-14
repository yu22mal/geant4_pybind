from geant4_pybind import *
import numpy as np

class StackingAction(G4UserStackingAction):

  def __init__(self, ph_cloud=[]):
    super().__init__()


  def ClassifyNewTrack(self, track):
    return G4ClassificationOfNewTrack.fUrgent
