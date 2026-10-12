"""Piezas reutilizables por los controladores."""


class PropietarioMixin:
    """Limita las consultas de una vista genérica a los datos del usuario autenticado.

    `campo_propietario` es la ruta desde el modelo hasta su dueño: "usuario" para
    vehículos, "vehiculo__usuario" para registros. Como `get_object()` parte de
    `get_queryset()`, pedir un dato de otro usuario responde 404 sin revelar que existe.
    """

    campo_propietario = "usuario"

    def get_queryset(self):
        return super().get_queryset().filter(**{self.campo_propietario: self.request.user})
