class House:
    def __init__(self, owner, address, bedrooms):
        self.owner = owner
        self.address = address
        self.last_price = None
        self.bedrooms = bedrooms
        self.for_sale = False

    def advertise(self):
        self.for_sale = True

    def sell(self, owner, price):
        if not self.for_sale:
            raise Exception
        self.owner = owner
        self.last_price = price

    # def __str__(self):
    #     return ' | '.join([self.owner, self.address, str(self.last_price), str(self.bedrooms), str(self.for_sale)])

# Rob built a mansion with 6 bedrooms
mansion = House("Rob", "123 Fake St, Kensington", 6)

# Viv built a 3 bedroom bungalow
bungalow = House("Viv", "42 Wallaby Way, Sydney", 3)

# The bungalow is advertised for sale
bungalow.advertise()

# Hayden tries to buy the mansion but can't
try:
    mansion.sell("Hayden", 3000000)
except Exception:
    print("Hayden is sad")

# He settles for buying the Bungalow instead
bungalow.sell("Hayden", 1000000)