
class Messanger:
    id: str
    name: str

    def __init__(self, jsonData) -> None:
        self.id = jsonData.get("id")
        self.type = jsonData.get("type")