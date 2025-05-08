"""
Modelos de SQLAlchemy para MySQL según el nuevo esquema.
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.db.database import Base


class UsuarioModel(Base):
    """Modelo de usuario para SQLAlchemy."""
    __tablename__ = "tableUSUARIO"

    idUSUARIO = Column(Integer, primary_key=True, autoincrement=True, index=True)
    idCLIENTE_FK = Column(Integer, ForeignKey("tableCLIENTE.idCLIENTE"), nullable=True)
    numero_clienteUSUARIO = Column(String(10), nullable=True)
    nombre_completoUSUARIO = Column(String(45), nullable=False)
    emailUSUARIO = Column(String(320), unique=True, index=True, nullable=False)
    passwordUSUARIO = Column(String(255), nullable=False)
    fecha_movUSUARIO = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones
    cliente = relationship("ClienteModel", back_populates="usuarios")
    # Aquí definimos la relación con las órdenes, indicando la clave foránea
    ordenes = relationship("OrdenDeTrabajoModel", back_populates="usuario", foreign_keys="OrdenDeTrabajoModel.idUSUARIO_FK")


class ClienteModel(Base):
    """Modelo de cliente para SQLAlchemy."""
    __tablename__ = "tableCLIENTE"

    idCLIENTE = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombreCLIENTE = Column(String(45), nullable=False)
    fecha_movCLIENTE = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones
    usuarios = relationship("UsuarioModel", back_populates="cliente")
    ordenes = relationship("OrdenDeTrabajoModel", back_populates="cliente")


class ProductoModel(Base):
    """Modelo de producto para SQLAlchemy."""
    __tablename__ = "tablePRODUCTO"

    idPRODUCTO = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tipoPRODUCTO = Column(String(8), nullable=False)
    descripcionPRODUCTO = Column(String(400), nullable=True)
    precioPRODUCTO = Column(Float, nullable=False)
    fecha_movPRODUCTO = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones
    ordenes = relationship("OrdenDeTrabajoModel", back_populates="producto")


class OrdenDeTrabajoModel(Base):
    """Modelo de orden de trabajo para SQLAlchemy."""
    __tablename__ = "tableORDENDETRABAJO"

    idORDENDETRABAJO = Column(Integer, primary_key=True, autoincrement=True, index=True)
    idCLIENTE_FK = Column(Integer, ForeignKey("tableCLIENTE.idCLIENTE"), nullable=False)
    idPRODUCTO_FK = Column(Integer, ForeignKey("tablePRODUCTO.idPRODUCTO"), nullable=False)
    # Agregar esta nueva columna como clave foránea
    idUSUARIO_FK = Column(Integer, ForeignKey("tableUSUARIO.idUSUARIO"), nullable=True)
    statusORDENDETRABAJO = Column(String(20), nullable=False)
    idPRODUCTO_linea1 = Column(Integer, nullable=True)
    cantidadPRODUCTO_linea1 = Column(Integer, nullable=True)
    precio_unitarioPRODUCTO_linea1 = Column(Float, nullable=True)
    # Aquí podrías añadir más líneas de productos según el diagrama

    # Relaciones
    cliente = relationship("ClienteModel", back_populates="ordenes")
    producto = relationship("ProductoModel", back_populates="ordenes")
    usuario = relationship("UsuarioModel", back_populates="ordenes", foreign_keys=[idUSUARIO_FK])