"""main entry point to have a dialogue with the user and an LLM"""

from core import config
from ui.cli import CLI
import ui.gui 

if __name__ == "__main__":
    conf = config.load_config(path="config.yml")

    if conf.ui == config.UI.CLI:
        interface = CLI(conf)
    elif conf.ui == config.UI.GUI:
        #temp hack
        interface = ui.gui
    else:
        raise NotImplementedError("Interface not implemented")

    interface.run()
