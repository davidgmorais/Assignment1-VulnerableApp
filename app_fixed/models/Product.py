class Product:
    def __init__(self, query_tuple) -> None:
        self.id = query_tuple[0]
        self.name = query_tuple[1]
        self.price = query_tuple[2]
        self.condition = query_tuple[11]
        self.category = query_tuple[9]
        self.description = query_tuple[5]
        self.image = query_tuple[6]

   