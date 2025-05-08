"""
Implementación del servicio de clientes.
"""
from typing import Dict, Any, Optional, List
from app.domain.ports.cliente_service import ClienteService
from app.domain.ports.cliente_repository import ClienteRepository
from app.domain.entities.cliente import Cliente


class ClienteServiceImpl(ClienteService):
    """Implementación del servicio de clientes."""

    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def create_cliente(self, cliente_data: Dict[str, Any]) -> Cliente:
        """Crea un nuevo cliente."""
        # Crear una nueva entidad de cliente
        new_cliente = Cliente(
            nombre=cliente_data["nombre"]
        )

        # Guardar el cliente en el repositorio
        return self.cliente_repository.save(new_cliente)

    def get_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """Obtiene un cliente por su ID."""
        return self.cliente_repository.find_by_id(cliente_id)

    def get_all_clientes(self) -> List[Cliente]:
        """Obtiene todos los clientes."""
        return self.cliente_repository.find_all()

    def update_cliente(self, cliente_id: int, cliente_data: Dict[str, Any]) -> Cliente:
        """Actualiza un cliente."""
        # Buscar el cliente existente
        existing_cliente = self.cliente_repository.find_by_id(cliente_id)
        if not existing_cliente:
            raise ValueError(f"Cliente con ID {cliente_id} no encontrado")

        # Actualizar los datos del cliente
        existing_cliente.nombre = cliente_data["nombre"]

        # Guardar los cambios
        return self.cliente_repository.update(existing_cliente)

    def delete_cliente(self, cliente_id: int) -> bool:
        """Elimina un cliente."""
        return self.cliente_repository.delete(cliente_id)