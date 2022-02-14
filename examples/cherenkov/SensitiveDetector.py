from geant4_pybind import *

class SensitiveDetector(G4VSensitiveDetector):

  def __init__(self, name):
    super().__init__(name)
    self.process_dict = {}


  def Initialize(self, hc):
    pass

  def ProcessHits(self, aStep, rohistory):
    aTrack = aStep.GetTrack()
    particle_def = aTrack.GetDefinition()
    if particle_def != G4OpticalPhoton.OpticalPhoton():
      return True
    # if photon:
    ene = aTrack.GetTotalEnergy()
    process = aStep.GetPostStepPoint().GetProcessDefinedStep()
    if process:
      process_name = process.GetProcessName()
    else:
      process_name = None
    if process_name not in self.process_dict.keys():
      self.process_dict[process_name] = 1
    else:
      self.process_dict[process_name] += 1
    return True


  def EndOfEvent(self, hc):
    self.Print()


  def Print(self):
    print(self.process_dict)

