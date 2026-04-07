# app/models.py

class Dog:
    # Agregamos image_url a los parámetros
    def __init__(self, dog_id, name, age, breed, image_url, adopted=False):
        self.id = dog_id
        self.name = name
        self.age = age
        self.breed = breed
        self.image_url = image_url  # <-- NUEVO
        self.adopted = adopted

class Adopter:
    def __init__(self, adopter_id, name, lastName, address, id_card=None):
        self.adopter_id = adopter_id
        self.name = name
        self.lastName = lastName
        self.address = address
        self.id_card = id_card