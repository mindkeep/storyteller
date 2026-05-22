"""Main entry point for StoryTeller.

Usage:
  python main.py         # CLI interface
  python main.py --gui   # Flet desktop app
"""

import sys
from dotenv import load_dotenv

if __name__ == "__main__":
    if "--gui" in sys.argv:
        import ui.gui
        ui.gui.run()
    else:
        load_dotenv()
        from ui.cli import CLI
        CLI().run()
