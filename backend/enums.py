from enum import StrEnum


class CurrencyEnum(StrEnum):
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"

    def __len__(self):
        return len(self.__members__)


class CategoryEnum(StrEnum):
    BILLS = "Bills"
    CAR = "Car"
    CLOTHES = "Clothes"
    COMMUNICATION = "Communication"
    EATING_OUT = "Eating out"
    ENTERTAINMENT = "Entertainment"
    FOOD = "Food"
    GIFTS = "Gifts"
    HEALTH = "Health"
    HOUSE = "House"
    PETS = "Pets"
    SPORT = "Sport"
    TAXI = "Taxi"
    TOILETRY = "Toiletry"
    TRANSPORT = "Transport"
    TRAVEL = "Travel"

    def __len__(self):
        return len(self.__members__)
