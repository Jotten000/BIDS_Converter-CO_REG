from packages.Elliot import UI_CO_REG
from chmod_on_startup_app import run_mac_startupp
import sys


# if sys.platform == 'darwin': ### Mac: needs to do chmod commands for used binary files
#     run_mac_startupp()


UI_CO_REG.start()