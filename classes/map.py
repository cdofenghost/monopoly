from .fields import (
    Field,
    Taxes,
    Jail,
    PoliceDepartment,
    Casino,
    Start,
    Chance,
    Property,
    GameBusiness,
    Company,
    CarBusiness,
)

class Map():
    def __init__(self):
        self.map = list[Field]

    def load_map(self):
        self.map.clear()

        # Upper Road
        self.map.append(Start())
        self.map.append(Company())
        self.map.append(Chance())
        self.map.append(Taxes())
        self.map.append(CarBusiness())
        self.map.append(Company())
        self.map.append(Chance())
        self.map.append(Company())
        self.map.append(Company())
        self.map.append(PoliceDepartment())

        # Right Road
        self.map.append(Company())
        self.map.append(GameBusiness())
        self.map.append(Company())
        self.map.append(Company())
        self.map.append(Company())
        self.map.append(Company())
        self.map.append(Chance())
        self.map.append(Company())
        self.map.append(Company())
        self.map.append(Casino())

        # Lower Road
        self.map.append(Company())
        self.map.append(Chance())
        self.map.append(Company())
        self.map.append(Company())
        self.map.append(CarBusiness())
        self.map.append(Company())
        self.map.append(Company())
        self.map.append(GameBusiness())
        self.map.append(Company())
        self.map.append(Jail())

        # Left Road
        self.map.append(Company())
        self.map.append(Company())
        self.map.append(Chance())
        self.map.append(Company())
        self.map.append(CarBusiness())
        self.map.append(Taxes())
        self.map.append(Company())
        self.map.append(Chance())
        self.map.append(Company())