from PySide6.QtCore import QAbstractTableModel, QModelIndex
from PySide6.QtGui import Qt

from logic.config import properties
from logic.database import find_all_of
from logic.model import Toolbox
from views.helpers import contains_search_text


class SearchTableModel(QAbstractTableModel):
    def __init__(self, col_count, search: str = "", items=None):
        super(SearchTableModel, self).__init__()
        self.col_count = col_count
        self.search = search.lower()  # Normalize to lowercase for easier matching
        if items is None:
            items = []
        self.all_items = items  # Store full, unfiltered list of items
        self.items = self.filter_items()  # Start with filtered list

    def set_search(self, search: str):
        """Update the search string and reapply filtering."""
        self.search = search.lower()
        self.items = self.filter_items()
        self.layoutChanged.emit()  # Notify the view that the data has changed

    def filter_items(self):
        """Filter items based on the search string. Must be implemented by subclasses."""
        return self.all_items

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return self.col_count

    def data(self, index, role=Qt.DisplayRole):
        """Must be implemented by subclass."""
        pass

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Must be implemented by subclass."""
        pass


class ToolboxModel(SearchTableModel):
    def __init__(self, search: str = ""):
        items = find_all_of(Toolbox)
        super(ToolboxModel, self).__init__(4, search, items)

    def filter_items(self):
        """Filter persons based on the search string."""
        if not self.search:
            return self.all_items  # No search; return all items

        # Normalize search value to lowercase for case-insensitive matching
        search_lower = self.search.lower()
        filtered = []
        for tb in self.all_items:
            # Decrypt fields when necessary and match them against the search string
            name = tb.name.lower()
            image= tb.image.lower()
            status = tb.status.lower()

            items = [name, image, status]
            match = contains_search_text(search_lower, items)

            if match:
                filtered.append(tb)

        return filtered

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            toolbox: Toolbox = self.items[index.row()]
            column = index.column()
            if column == 0:
                return toolbox.id
            elif column == 1:
                return toolbox.name
            elif column == 2:
                return toolbox.image
            elif column == 3:
                return toolbox.status
            elif column == 4:
                return toolbox.created_at
            elif column == 5:
                return toolbox.default
        return None


def headerData(self, section, orientation, role=Qt.DisplayRole):
    if role == Qt.DisplayRole and orientation == Qt.Horizontal:
        if section == 0:
            return "ID"
        elif section == 1:
            return self.tr("Name")
        elif section == 2:
            return self.tr("Image")
        elif section == 3:
            return self.tr("Status")
        elif section == 4:
            return self.tr("Created At")
        elif section == 5:
            return self.tr("Default")

    return None
