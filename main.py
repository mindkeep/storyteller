"""main entry point to have a dialogue with the user and an LLM"""

from core import config
from ui.cli import CLI

if __name__ == "__main__":
    conf = config.load_config(path="config.yml")

    if conf.ui == config.UI.CLI:
        interface = CLI(conf)
    else:
        raise NotImplementedError("Interface not implemented")

    interface.run()
