class Case:
    """Класс для представления записи об обращении на ремонт остановки.
    Все поля обязательны и должны быть строками (str)."""
    
    def __init__(
        self,
        id: str,
        code: str,
        description: str,
        addres: str,
        status_name: str,
        coordinator_name: str | None,
        owner_name: str | None,
        image: str | None,
        location: str | None,
        initiator_name: str,
        name: str
    ):
        self.id = id
        self.code = code
        self.description = description
        self.addres = addres
        self.status_name = status_name
        self.coordinator_name = coordinator_name
        self.owner_name = owner_name
        self.image = image
        self.location = location
        self.initiator_name = initiator_name
        self.name = name
