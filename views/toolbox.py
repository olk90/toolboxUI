from PySide6.QtWidgets import QWidget, QMessageBox, QLineEdit, QTableView, \
    QComboBox, QDateEdit, QCheckBox

from logic.database import persist_item, delete_item, find_by_id, update_toolbox
from logic.model import Toolbox
from logic.table_models import ToolboxModel
from views.base_classes import TableDialog, EditorDialog, EditorWidget, CenteredItemDelegate
from views.confirmationDialogs import ConfirmDeletionDialog


class AddToolboxDialog(EditorDialog):

    def __init__(self, parent: QWidget):
        super(AddToolboxDialog, self).__init__(parent=parent, ui_file_name="ui/toolboxEditor.ui")

        # self.get_widget(QLabel, "editorTitle").setText(self.tr("Add Person"))
        #
        # self.firstname_edit: QLineEdit = self.get_widget(QLineEdit, "firstNameEdit")
        # self.lastname_edit: QLineEdit = self.get_widget(QLineEdit, "lastNameEdit")
        #
        # self.firstname_edit.textChanged.connect(self.widget.validate)
        # self.lastname_edit.textChanged.connect(self.widget.validate)
        #
        # self.widget.append_validation_fields(self.firstname_edit, self.lastname_edit)
        #
        # self.email_edit: QLineEdit = self.get_widget(QLineEdit, "emailEdit")
        #
        # self.layout = QHBoxLayout(self)
        # self.layout.addWidget(self.widget)
        # self.button_box: QDialogButtonBox = self.widget.buttonBox

        self.configure_widgets()

    def commit(self):
        first_name: str = self.firstname_edit.text()
        last_name: str = self.lastname_edit.text()
        email: str = self.email_edit.text()

        tb = Toolbox(firstname=first_name, lastname=last_name, email=email)
        persist_item(tb)
        self.parent.reload_table_contents(model=ToolboxModel())
        self.close()


class ToolboxEditorWidget(EditorWidget):

    def __init__(self, item_id=None):
        super(ToolboxEditorWidget, self).__init__(ui_file_name="ui/toolboxEditor.ui", item_id=item_id)

        self.name_edit: QLineEdit = self.widget.nameEdit
        self.image_edit: QLineEdit = self.widget.imageEdit
        self.status_cb: QComboBox = self.widget.statusComboBox
        self.created_at_Edit: QDateEdit = self.widget.createdAtEdit
        self.default_cb: QCheckBox = self.widget.defaultCheckBox

    def fill_fields(self, tb: Toolbox):
        self.item_id = tb.id

        self.name_edit.setText(tb.name)
        self.image_edit.setText(tb.image)
        self.status_cb.setCurrentText(tb.status)
        self.created_at_Edit.setDate(tb.created_at)
        self.default_cb.setChecked(tb.default)

    def get_values(self) -> dict:
        return {
            "item_id": self.item_id,
            "name": self.name_edit.text(),
            "image": self.image_edit.text(),
            "status": self.status_cb.currentText(),
            "created_at": self.created_at_Edit.date().toString("yyyy-MM-dd"),
            "default": self.default_cb.isChecked(),
        }

    def clear_fields(self):
        self.name_edit.clear()
        self.image_edit.clear()
        self.status_cb.setCurrentIndex(0)
        self.created_at_Edit.clear()
        self.default_cb.setChecked(False)
        self.toggle_buttons(False)


class ToolboxWidget(TableDialog):

    def __init__(self):
        super(ToolboxWidget, self).__init__()
        self.add_dialog = AddToolboxDialog(self)
        self.setup_table(ToolboxModel(), range(1, 4))

        tableview: QTableView = self.get_table()
        delegate = CenteredItemDelegate()
        tableview.setItemDelegate(delegate)

    def get_editor_widget(self) -> EditorWidget:
        return ToolboxEditorWidget()

    def delete_item(self):
        dialog = ConfirmDeletionDialog(self)
        button = dialog.exec_()
        if button == QMessageBox.AcceptRole:
            tb: Toolbox = self.get_selected_item()
            delete_item(tb)
            search = self.search_line.text()
            self.reload_table_contents(model=ToolboxModel(search))
            self.editor.clear_fields()

    def get_selected_item(self):
        item_id = super().get_selected_item()
        tb = find_by_id(item_id, Toolbox)
        return tb

    def commit_changes(self):
        value_dict: dict = self.editor.get_values()
        update_toolbox(value_dict)
        search = self.search_line.text()
        self.reload_table_contents(model=ToolboxModel(search))
        self.editor.clear_fields()

    def revert_changes(self):
        tb: Toolbox = find_by_id(self.editor.item_id, Toolbox)
        self.editor.fill_fields(tb)
