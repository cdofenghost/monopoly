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
        self.map.append(Company(name="Chanel", type="Парфюмерия", price=600, rent=20, rent_sheet={1: 100, 2: 300, 3: 900, 4: 1600, 5: 2500}))
        self.map.append(Chance())
        self.map.append(Company(name="Hugo Boss", type="Парфюмерия", price=600, rent=40, rent_sheet={1: 200, 2: 600, 3: 1800, 4: 3200, 5: 4500}))
        self.map.append(Taxes())
        self.map.append(CarBusiness(name="Mercedes", price=2000, rent=250))
        self.map.append(Company(name="Adidas", type="Одежда", price=1000, rent=60, rent_sheet={1: 300, 2: 900, 3: 2700, 4: 4000, 5: 5500}))
        self.map.append(Chance())
        self.map.append(Company(name="Puma", type="Одежда", price=1000, rent=60, rent_sheet={1: 300, 2: 900, 3: 2700, 4: 4000, 5: 5500}))
        self.map.append(Company(name="Lacoste", type="Одежда", price=1200, rent=80, rent_sheet={1: 400, 2: 1000, 3: 3000, 4: 4500, 5: 6000}))
        self.map.append(PoliceDepartment())

        # Left Road
        self.map.append(Company(name="VK", type="Социальные сети", price=1400, rent=100, rent_sheet={1: 500, 2: 1500, 3: 4500, 4: 6200, 5: 7500}))
        self.map.append(GameBusiness(name="Rockstar Games", type="Игры", price=1500, rent=150, multiplier=1.5))
        self.map.append(Company(name="Facebook", type="Социальные сети", price=1400, rent=100, rent_sheet={1: 500, 2: 1500, 3: 4500, 4: 6200, 5: 7500}))
        self.map.append(Company(name="Twitter", type="Социальные сети", price=1600, rent=120, rent_sheet={1: 600, 2: 1800, 3: 5000, 4: 7000, 5: 9000}))
        self.map.append(CarBusiness(name="Audi", price=2000, rent=250))
        self.map.append(Company(name="Coca-Cola", type="Напитки", price=1800, rent=140, rent_sheet={1: 700, 2: 2000, 3: 5500, 4: 7500, 5: 9500}))
        self.map.append(Chance())
        self.map.append(Company(name="Pepsi", type="Напитки", price=1800, rent=140, rent_sheet={1: 700, 2: 2000, 3: 5500, 4: 7500, 5: 9500}))
        self.map.append(Company(name="Fanta", type="Напитки", price=2000, rent=160, rent_sheet={1: 700, 2: 2000, 3: 5500, 4: 7500, 5: 9500}))

        # Lower Road
        self.map.append(Casino())
        self.map.append(Company(name="British Airways", type="Авиакомпании", price=2200, rent=180, rent_sheet={1: 900, 2: 2500, 3: 7000, 4: 8750, 5: 10500}))
        self.map.append(Chance())
        self.map.append(Company(name="Lufthansa", type="Авиакомпании", price=2200, rent=180, rent_sheet={1: 900, 2: 2500, 3: 7000, 4: 8750, 5: 10500}))
        self.map.append(Company(name="American Airlines", type="Авиакомпании", price=2400, rent=200, rent_sheet={1: 1000, 2: 3000, 3: 7500, 4: 9250, 5: 11000}))
        self.map.append(CarBusiness(name="Ford", price=250, rent=150))
        self.map.append(Company(name="McDonald's", type="Фастфуд", price=2600, rent=220, rent_sheet={1: 1100, 2: 3300, 3: 8000, 4: 9750, 5: 11500}))
        self.map.append(Company(name="Burger King", type="Фастфуд", price=2600, rent=220, rent_sheet={1: 1100, 2: 3300, 3: 8000, 4: 9750, 5: 11500}))
        self.map.append(GameBusiness(name="Rovio", type="Игры", price=1500, rent=150, multiplier=1.5))
        self.map.append(Company(name="KFC", type="Фастфуд", price=2800, rent=240, rent_sheet={1: 1200, 2: 3600, 3: 8500, 4: 10250, 5: 12000}))
        self.map.append(Jail())

        # Right Road
        self.map.append(Company(name="Holiday Inn", type="Отели", price=3000, rent=260, rent_sheet={1: 1300, 2: 3900, 3: 9000, 4: 11000, 5: 12750}))
        self.map.append(Company(name="Radisson Blue", type="Отели", price=3000, rent=260, rent_sheet={1: 1300, 2: 3900, 3: 9000, 4: 11000, 5: 12750}))
        self.map.append(Chance())
        self.map.append(Company(name="Novotel", type="Отели", price=3200, rent=280, rent_sheet={1: 1500, 2: 4500, 3: 10000, 4: 12000, 5: 14000}))
        self.map.append(CarBusiness(name="Land Rover", price=2000, rent=250))
        self.map.append(Taxes())
        self.map.append(Company(name="Apple", type="Смартфоны", price=3500, rent=350, rent_sheet={1: 1750, 2: 5000, 3: 11000, 4: 13000, 5: 15000}))
        self.map.append(Chance())
        self.map.append(Company(name="Nokia", type="Смартфоны", price=4000, rent=500, rent_sheet={1: 2000, 2: 6000, 3: 14000, 4: 17000, 5: 20000}))