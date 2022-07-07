import csv, gzip
from typing import Tuple

from functions import normalize_price

_file_path = './files/listings.csv.gz'

def get_listings_data(calendar_data: dict) -> Tuple[dict, list, list]:
    """
    Reads the listings file and processes it, obtaining only
    the relevant information

    If a listing doesn't have corresponding information for the occupancy, price
    or rating it is not included

    Returns:
        The information related to the average occupancy, average price
    and average rating of a listing in Airbnb organized by neighbourhood
    and room type
    """

    data = {}
    neighbourhoods = []
    room_types = []

    with gzip.open(_file_path, 'rt', encoding='utf-8') as listings:
        listings_reader = csv.reader(listings, delimiter=',')

        listings_header = next(listings_reader)

        listing_id_index = listings_header.index('id')
        listing_price_index = listings_header.index('price')
        listing_rating_index = listings_header.index('review_scores_rating')
        listing_neighbourhood_index = listings_header.index('neighbourhood_cleansed')
        listing_room_type_index = listings_header.index('room_type')

        for row in listings_reader:
            listing_id = row[listing_id_index]
            if listing_id not in calendar_data.keys():
                continue

            price = row[listing_price_index]
            if price == '':
                continue

            rating = row[listing_rating_index]
            if rating == '':
                continue

            price = normalize_price(price)
            rating = float(rating)
            neighbourhood = row[listing_neighbourhood_index]
            room_type = row[listing_room_type_index]
            occupancy_percentage = calendar_data[listing_id] / 365

            if neighbourhood not in data.keys():
                data[neighbourhood] = {
                    room_type: {
                        'occupancy_percentage_sum': 0,
                        'price_sum': 0,
                        'rating_sum': 0,
                        'counter': 0
                    }
                }

            if room_type not in data[neighbourhood].keys():
                data[neighbourhood][room_type] = {
                    'occupancy_percentage_sum': 0,
                    'price_sum': 0,
                    'rating_sum': 0,
                    'counter': 0
                }

            data[neighbourhood][room_type]['occupancy_percentage_sum'] += occupancy_percentage
            data[neighbourhood][room_type]['price_sum'] += price
            data[neighbourhood][room_type]['rating_sum'] += rating
            data[neighbourhood][room_type]['counter'] += 1

            if neighbourhood not in neighbourhoods:
                neighbourhoods.append(neighbourhood)
            if room_type not in room_types:
                room_types.append(room_type)

    return (data, neighbourhoods, room_types)