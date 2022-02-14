from geant4_pybind import *
import sys

from ActionInitialization import ActionInitialization
from DetectorConstruction import DetectorConstruction
from CustomPhysicsList import CustomPhysicsList

# Detect interactive mode (if no arguments) and define UI session
ui = None
if len(sys.argv) == 1:
    ui = G4UIExecutive(len(sys.argv), sys.argv)

# Construct the default run manager
runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.MT, 4)  #.Serial)

# Set mandatory initialization classes
runManager.SetUserInitialization(DetectorConstruction())
runManager.SetUserInitialization(CustomPhysicsList())
runManager.SetUserInitialization(ActionInitialization())

# Initialize visualization
visManager = G4VisExecutive()
# G4VisExecutive can take a verbosity argument - see /vis/verbose guidance.
# visManager = G4VisExecutive("Quiet");
visManager.Initialize()

# Get the pointer to the User Interface manager
UImanager = G4UImanager.GetUIpointer()

# Process macro or start UI session
if ui == None:
    # batch mode
    command = "/control/execute "
    fileName = sys.argv[1]
    UImanager.ApplyCommand(command+fileName)
else:
    # interactive mode
    UImanager.ApplyCommand("/control/execute init_vis.mac")
    ui.SessionStart()
