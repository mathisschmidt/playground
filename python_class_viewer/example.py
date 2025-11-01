from typing import List, Optional

class Animal:
    def __init__(self, name: str, age: int):
        self.name: str = name
        self.age: int = age

    def make_sound(self) -> str:
        return "Generic animal sound"

    def get_info(self) -> dict:
        return {"name": self.name, "age": self.age}

class Dog(Animal):
    breed: str
    toys: List[str]

    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)
        self.breed = breed
        self.toys = []

    def make_sound(self) -> str:
        return "Woof!"

    def add_toy(self, toy_name: str) -> None:
        self.toys.append(toy_name)

    def play_fetch(self, item: str) -> bool:
        return True

class Cat(Animal):
    lives_remaining: int = 9
    favorite_food: Optional[str] = None

    def make_sound(self) -> str:
        return "Meow!"

    def purr(self) -> None:
        pass

    def chase_laser(self, speed: float) -> bool:
        return speed < 10.0

class PetShop:
    def __init__(self):
        self.pets: List[Animal] = []
        self.location: str = ""

    def add_pet(self, pet: Animal) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        return True

    def get_all_pets(self) -> List[Animal]:
        return self.pets

    def count_pets(self) -> int:
        return len(self.pets)
