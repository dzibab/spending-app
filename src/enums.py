from enum import StrEnum


# Default currencies enum
class CurrencyEnum(StrEnum):
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"


# Default categories enum
class CategoryEnum(StrEnum):
    CAR = "Car"
    FOOD = "Food"
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Entertainment"
    EATING_OUT = "Eating Out"
    HEALTH = "Health"
    CLOTHES = "Clothes"
    TRAVEL = "Travel"
    HOUSE = "House"
    GIFTS = "Gifts"
    COMMUNICATION = "Communication"
