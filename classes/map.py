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
        self.map: list[Field] = []

    def load_map(self):
        self.map.clear()

        # Upper Road
        self.map.append(Start())
        self.map.append(Company(name="Chanel", type="Парфюмерия", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Chance())
        self.map.append(Company(name="Hugo Boss", type="Парфюмерия", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Taxes())
        self.map.append(CarBusiness(name="Mercedes", price=150, rent=150))
        self.map.append(Company(name="Adidas", type="Одежда", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Chance())
        self.map.append(Company(name="Puma", type="Одежда", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Company(name="Lacoste", type="Одежда", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(PoliceDepartment())

        # Left Road
        self.map.append(Company(name="VK", type="Социальные сети", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(GameBusiness(name="Rockstar Games", type="Игры", price=150, rent=150, multiplier=1.5))
        self.map.append(Company(name="Facebook", type="Социальные сети", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Company(name="Twitter", type="Социальные сети", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(CarBusiness(name="Audi", price=150, rent=150))
        self.map.append(Company(name="Coca-Cola", type="Напитки", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Chance())
        self.map.append(Company(name="Pepsi", type="Напитки", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Company(name="Fanta", type="Напитки", price=150, rent=150, rent_sheet={0: 150, 1: 300}))

        # Lower Road
        self.map.append(Casino())
        self.map.append(Company(name="British Airways", type="Авиакомпании", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Chance())
        self.map.append(Company(name="Lufthansa", type="Авиакомпании", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Company(name="American Airlines", type="Авиакомпании", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(CarBusiness(name="Ford", price=150, rent=150))
        self.map.append(Company(name="McDonald's", type="Фастфуд", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Company(name="Burger King", type="Фастфуд", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(GameBusiness(name="Rovio", type="Игры", price=150, rent=150, multiplier=1.5))
        self.map.append(Company(name="KFC", type="Фастфуд", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Jail())

        # Right Road
        self.map.append(Company(name="Holiday Inn", type="Отели", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Company(name="Radisson Blue", type="Отели", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Chance())
        self.map.append(Company(name="Novotel", type="Отели", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(CarBusiness(name="Land Rover", price=150, rent=150))
        self.map.append(Taxes())
        self.map.append(Company(name="Apple", type="Смартфоны", price=150, rent=150, rent_sheet={0: 150, 1: 300}))
        self.map.append(Chance())
        self.map.append(Company(name="Nokia", type="Смартфоны", price=150, rent=150, rent_sheet={0: 150, 1: 300}))