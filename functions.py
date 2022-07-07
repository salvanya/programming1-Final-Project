import os
import platform
from typing import List

def average(summation: float, quantity: int) -> float:
    """
    Calculates the average for a summation and a quantity
    rounded up to 2 decimals

    Arguments:
        summation: a float representing a summation
        quantity: a float representing a quantity

    Returns:
        The average for a summation of a quantity of values
    """

    average = round(summation / quantity , 2)
    return average

def normalize_str(input: str) -> str:
    """
    Normalizes the input, making it all capital letters and
    replacing blank spaces and slashes with underscores

    Arguments:
        input: a string representing the text that will be normalized

    Returns:
        The normalized input
    """

    return input.upper().replace(' ', '_').replace('/', '_')

def normalize_str_list(input: List[str]) -> dict:
    """
    Normalizes the input, making all its items capital letters and
    replacing blank spaces and slashes with underscores

    Arguments:
        input: a list containing the text items that will be normalized

    Returns:
        The normalized input
    """

    normalized_input = {}

    for input_item in input:
        normalized_room_type = normalize_str(input_item)
        if normalized_room_type not in normalized_input.keys():
            normalized_input[normalized_room_type] = input_item

    return normalized_input

def normalize_price(price: str) -> float:
    """
    Normalizes the price, removing the monetary sign ($, €, £, etc.)
    from the beggining of the text and removing the commas

    Arguments:
        price: a string representing the price that will be normalized

    Returns:
        The normalized price
    """

    return float(price[1:].replace(',',''))

def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')