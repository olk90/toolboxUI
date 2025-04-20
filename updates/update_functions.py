from logic.config import properties
from logic.database import persist_item


def dummy_update():
    """Example of an update function"""
    s = properties.open_session()
    # Update code to be inserted
    s.commit()
