from geant4_pybind import *
from RunAction import RunAction
from PrimaryGeneratorAction import PrimaryGeneratorAction
from StackingAction import StackingAction

class ActionInitialization(G4VUserActionInitialization):

    def BuildForMaster(self):
        self.SetUserAction(RunAction(True))

    def Build(self):
        self.SetUserAction(PrimaryGeneratorAction())
        self.SetUserAction(RunAction(False))
        self.SetUserAction(StackingAction())
