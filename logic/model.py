from sqlalchemy import (Column, Integer, String, Boolean, Date, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
toolboxTableName = "Toolbox"
inventoryTableName = "InventoryItem"
versionInfoTableName = "VersionInfo"
encryptionStateName = "EncryptionState"


class Toolbox(Base):
    __tablename__ = toolboxTableName

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # Name of the toolbox
    image = Column(String(200), nullable=False)  # Image used by toolbox
    status = Column(String(50), nullable=False)  # Status of the toolbox (e.g., "running", "stopped")
    created_at = Column(Date, nullable=False)  # Date when the toolbox was created
    default = Column(Boolean, nullable=False, default=False)  # Whether this is the default toolbox

    def __repr__(self):
        return f"<Toolbox(name='{self.name}', image='{self.image}', status='{self.status}', created_at='{self.created_at}', default={self.default})>"


class VersionInfo(Base):
    __tablename__ = versionInfoTableName

    id = Column(Integer, primary_key=True)
    version = Column(Integer, nullable=False, default=0)


class EncryptionState(Base):
    __tablename__ = encryptionStateName

    id = Column(Integer, primary_key=True)
    encryption_state = Column(Boolean, nullable=False)


def create_tables(engine):
    Base.metadata.create_all(engine)
