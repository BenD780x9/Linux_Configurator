#!/usr/bin/env python

import sys

from config_gui import *
from logic.facts import Facts


def main():
    facts = Facts()
    if not is_sudo():
        print("This script must be run as root") # replace with a QMessageBox not DEBUG
        sys.exit()

    facts.collect_facts()
    app = QApplication(sys.argv)
    win = MainWindow(facts)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
