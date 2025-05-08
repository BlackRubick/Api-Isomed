"""
Implementación del servicio de órdenes de trabajo.
"""
from typing import Dict, Any, Optional, List
from app.domain.ports.orden_trabajo_service import OrdenTrabajoService
from app.domain.ports.orden_trabajo_repository import OrdenTrabajoRepository
from app.domain.entities.orden_trabajo import OrdenDeTrabajo, LineaProducto


class OrdenTrabajoServiceImpl(OrdenTrabajoService):
    """Implementación del servicio de órdenes de trabajo."""

    def __init__(self, orden_repository: OrdenTrabajoRepository):
        self.orden_repository = orden_repository

    def create_orden(self, orden_data: Dict[str, Any]) -> OrdenDeTrabajo:
        """Crea una nueva orden de trabajo."""
        # Crear líneas de producto
        lineas_producto = []
        for linea_data in orden_data.get("lineas_producto", []):
            linea = LineaProducto(
                id_producto=linea_data["id_producto"],
                cantidad=linea_data["cantidad"],
                precio_unitario=linea_data["precio_unitario"]
            )
            lineas_producto.append(linea)

        # Crear una nueva entidad de orden de trabajo
        new_orden = OrdenDeTrabajo(
            id_cliente=orden_data["id_cliente"],
            id_producto=orden_data["id_producto"],
            status=orden_data.get("status", "pendiente"),
            lineas_producto=lineas_producto
        )

        # Guardar la orden en el repositorio
        return self.orden_repository.save(new_orden)

    def get_orden(self, orden_id: int) -> Optional[OrdenDeTrabajo]:
        """Obtiene una orden de trabajo por su ID."""
        return self.orden_repository.find_by_id(orden_id)

    def get_ordenes_by_cliente(self, cliente_id: int) -> List[OrdenDeTrabajo]:
        """Obtiene todas las órdenes de trabajo de un cliente."""
        return self.orden_repository.find_by_cliente_id(cliente_id)

    def get_all_ordenes(self) -> List[OrdenDeTrabajo]:
        """Obtiene todas las órdenes de trabajo."""
        return self.orden_repository.find_all()

    def update_orden(self, orden_id: int, orden_data: Dict[str, Any]) -> OrdenDeTrabajo:
        """Actualiza una orden de trabajo."""
        # Buscar la orden existente
        existing_orden = self.orden_repository.find_by_id(orden_id)
        if not existing_orden:
            raise ValueError(f"Orden de trabajo con ID {orden_id} no encontrada")

        # Actualizar los datos de la orden
        existing_orden.id_cliente = orden_data.get("id_cliente", existing_orden.id_cliente)
        existing_orden.id_producto = orden_data.get("id_producto", existing_orden.id_producto)
        existing_orden.status = orden_data.get("status", existing_orden.status)

        # Actualizar líneas de producto si se proporcionan
        if "lineas_producto" in orden_data:
            lineas_producto = []
            for linea_data in orden_data["lineas_producto"]:
                linea = LineaProducto(
                    id_producto=linea_data["id_producto"],
                    cantidad=linea_data["cantidad"],
                    precio_unitario=linea_data["precio_unitario"]
                )
                lineas_producto.append(linea)
            existing_orden.lineas_producto = lineas_producto

        # Guardar los cambios
        return self.orden_repository.update(existing_orden)

    def delete_orden(self, orden_id: int) -> bool:
        """Elimina una orden de trabajo."""
        return self.orden_repository.delete(orden_id)