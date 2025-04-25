import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QTabWidget)

from logic.load_data import load_data
from views.container import ContainersTab
from views.images import ImagesTab

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()

    # Create layout and widgets
    main_layout = QVBoxLayout()

    # Create a tab widget to hold both tables
    tab_widget = QTabWidget()
    tab_widget.setTabPosition(QTabWidget.TabPosition.West)

    # Tab for images table
    it = ImagesTab()
    tab_widget.addTab(it, "Images")

    # Tab for containers table
    ct = ContainersTab()
    tab_widget.addTab(ct, "Containers")

    # Add widgets to main layout
    main_layout.addWidget(tab_widget)
    window.setLayout(main_layout)

    # load data on app launch
    load_data(it.images_model, ct.containers_model, it.images_table, ct.containers_table)

    # Set window properties
    window.setWindowTitle("Toolbox UI")
    window.resize(1600, 900)
    window.show()
    sys.exit(app.exec())
