#!/usr/bin/env python

import sys

from config_gui import *
from logic.facts import Facts


def main():
    facts = Facts()

    """ Disable ONLY for testing """
    if not is_sudo():
        print("This script must be run as root")
        app = QApplication(sys.argv)
        msg = QMessageBox.critical(None,
                                  "RootError",
                                  "This script must be run as root",
                                  QMessageBox.Ok)
        sys.exit()

    facts.collect_facts()
    app = QApplication(sys.argv)
    win = MainWindow(facts)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 