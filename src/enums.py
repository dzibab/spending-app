from enum import StrEnum


# Default currencies enum
class Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"


# Default categories enum
class Category(StrEnum):
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
