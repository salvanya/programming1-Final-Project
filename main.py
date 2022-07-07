import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.axes import Axes
from typing import Iterator, List, Tuple

from airbnb_calendar import get_calendar_data
from airbnb_listings import get_listings_data
from functions import average, clear_screen, normalize_str, normalize_str_list

def main():
    (airbnb_data, neighbourhoods, room_types) = _read_airbnb_data()

    for neighbourhood in neighbourhoods:
        for room_type in room_types:
            (average_occupancy, average_price, average_rating) = \
                _filter_average_data_by_neighbourhood_by_room_type(airbnb_data,
                    neighbourhood,
                    room_type)

            _generate_plot_data(room_type, average_occupancy, average_price, average_rating)
    
    _display_menu(neighbourhoods, room_types)

def _display_menu(neighbourhoods: List[str], room_types: List[str]):
    """
    Creates the menu for the application

    Arguments:
        neighbourhoods: a list of strings representing the neighbourhoods
        room_types: a list of strings representing the room types
    """

    messi_color_palette = ['#0d24a6', '#ce3843', '#c8c2aa', '#462629']
    elegant_color_palette = ['#f79256', '#a53860','#1d4e89', '#4c3b4d']

    while(True):
        clear_screen()

        print('Data Analysis for Copenhagen')
        print('----------------------------')
        print('1) Price by Room Type by Neighbourhood')
        print('2) Rating by Room Type by Neighbourhood')
        print('3) Occupancy by Room Type by Neighbourhood')
        print('   and its relation with Price and Rating')
        print('0) Exit')
        user_selection = input('Select which graphic you would like to see: ')

        if user_selection == '1':
            title = 'Price by Room Type by Neighbourhood'
            y = 'price'
            _plot_question_one_and_two(neighbourhoods, room_types, y, title, elegant_color_palette)
        elif user_selection == '2':
            title = 'Rating by Room Type by Neighbourhood'
            y = 'rating'
            _plot_question_one_and_two(neighbourhoods, room_types, y, title, elegant_color_palette)
        elif user_selection == '3':
            _plot_question_three(neighbourhoods, room_types, messi_color_palette)
        elif user_selection == '0':
            break
        else:
            clear_screen()

            print('The selected option is not valid. Please select a valid option.')
            print()
            input('Press "Enter" to continue...')

def _read_airbnb_data() -> Tuple[dict, list, list]:
    """
    Reads the Airbnb files and merges them into a dictionary
    containing the average occupancy, average price and average rating
    organized by neighbourhood and room type

    Returns:
        A dictionary containing the average occupancy, average price and average
    rating organized by neighbourhood and room type
    """

    calendar_data = get_calendar_data()
    return get_listings_data(calendar_data)

def _filter_average_data_by_neighbourhood_by_room_type(data: dict, neighbourhood: str, room_type: str) -> Tuple[float, float, float]:
    """
    Filters the given data by neighbourhood and room type to find
    the average occupancy, average price and average rating

    Arguments:
        data: a dictionary representing the Airbnb data
        neighbourhood: a string representing the filtering neighbourhood
        room_type: a string representing the filtering room_type

    Returns:
        The average average occupancy, average price and average rating
    for the given data filtered by neighbourhood and room type
    """

    if room_type in data[neighbourhood].keys():
        occupancy_percentage_sum = data[neighbourhood][room_type]['occupancy_percentage_sum'] * 100
        price_sum = data[neighbourhood][room_type]['price_sum']
        rating_sum = data[neighbourhood][room_type]['rating_sum']
        counter = data[neighbourhood][room_type]['counter']
    else:
        occupancy_percentage_sum = np.nan
        price_sum = np.nan
        rating_sum = np.nan
        counter = 0

    if counter != 0:
        average_occupancy = average(occupancy_percentage_sum, counter)
        average_price = average(price_sum, counter)
        average_rating = average(rating_sum, counter)
    else:
        average_occupancy = np.nan
        average_price = np.nan
        average_rating = np.nan

    return (average_occupancy, average_price, average_rating)

def _generate_plot_data(room_type: str, average_occupancy: float, average_price: float, average_rating: float):
    """
    Generates the data needed for plotting. Given a room type and it's
    average occupancy, average price and average rating, it will generate
    the corresponding lists for each average value with the room type. If
    the list already exists, it will keep adding to its values. Correct use
    of this function requires that a matching neighbourhood list exists.

    Arguments:
        room_type: a string representing the room type
        average_occupancy: a float representing the average occupancy
        average_price: a float representing the average price
        average_rating: a float representing the average rating
    """

    normalized_room_type = normalize_str(room_type)

    if f'_{normalized_room_type}_occupancy' not in globals():
        globals()[f'_{normalized_room_type}_occupancy'] = []
    if f'_{normalized_room_type}_price' not in globals():
        globals()[f'_{normalized_room_type}_price'] = []
    if f'_{normalized_room_type}_rating' not in globals():
        globals()[f'_{normalized_room_type}_rating'] = []

    globals()[f'_{normalized_room_type}_occupancy'].append(average_occupancy)
    globals()[f'_{normalized_room_type}_price'].append(average_price)
    globals()[f'_{normalized_room_type}_rating'].append(average_rating)

def _plot_question_one_and_two(neighbourhoods: List[str], room_types: List[str], y: str, title: str, color_list: List[str]):
    sns.set()

    x = np.arange(len(neighbourhoods))
    width = 0.20
    normalized_room_types = normalize_str_list(room_types)

    fig, ax = plt.subplots()
    color_palette = iter(color_list)
    _plot_bars(normalized_room_types, color_palette, [ax], x, width, y)

    ax.set_title(title, fontsize = 14)
    ax.set_xticks(x, neighbourhoods, rotation = 90, fontsize = 10)
    ax.legend(loc='center left', bbox_to_anchor = (1, 0.5), fancybox = True, ncol = 1)
    
    if y == 'rating':
        ax.set_ylim([3.5, 5])

    fig.set_figheight(6)
    fig.set_figwidth(15)
    fig.tight_layout()
    
    plt.show()

def _plot_question_three(neighbourhoods: List[str], room_types: List[str], color_list: List[str]):
    sns.set()

    x = np.arange(len(neighbourhoods))
    width = 0.20
    normalized_room_types = normalize_str_list(room_types)

    fig, axs = plt.subplots(1, 2)
    twinxs = [axs[0].twinx(), axs[1].twinx()]
    ytwinxs = ['price', 'rating']
    color_palette = iter(color_list)
    twinx_color = '#140b34'

    _plot_bars(normalized_room_types, color_palette, [axs[0], axs[1]], x, width, 'occupancy')
    _plot_scatters(normalized_room_types, twinx_color, twinxs, x, ytwinxs, width)
    _plot_lines(neighbourhoods, normalized_room_types, twinx_color, twinxs, x, ytwinxs, width)

    axs[0].set_title('Occupancy and Price', fontsize = 14)
    axs[0].set_xticks(x, neighbourhoods, rotation = 90, fontsize = 10)
    axs[0].legend(loc='center left', bbox_to_anchor = (1.1, 0.5), fancybox = True, ncol = 1)

    axs[1].set_title('Occupancy and Rating', fontsize = 14)
    axs[1].set_xticks(x, neighbourhoods, rotation = 90, fontsize = 10)

    fig.set_figheight(6)
    fig.set_figwidth(15)
    fig.tight_layout()
    
    plt.show()

def _plot_bars(normalized_room_types: dict, color_palette: Iterator[str], axs: List[Axes], x: np.ndarray, width: float, y: str):
    """
    Generates bar graphs for the user to see based on the
    room types that it receives.

    Arguments:
        normalized_room_types: a dictionary containing the normalized room types
        color_palette: a list of the colors available for use
        axs: the axes for the graphs
        x: the arranged positions for the x axis
        width: the width of each bar
    """
    
    relative_distances = _get_relative_distances(width, normalized_room_types.keys())

    for normalized_room_type in normalized_room_types.keys():
        values = globals()[f'_{normalized_room_type}_{y}']

        selected_color = next(color_palette)

        for ax in axs:
            ax.bar(x + relative_distances[normalized_room_type], values, width, label=normalized_room_types[normalized_room_type], color = selected_color)

def _plot_scatters(normalized_room_types: dict, color: str, axs: List[Axes], x: np.ndarray, y: List[str], width: float, marker = 'd', linewidths = 1.5):
    """
    Generates scatter graphs for the user to see based on the
    room types that it receives.

    Arguments:
        normalized_room_types: a dictionary containing the normalized room types
        color: a str representing the color for the graph
        axs: the axes for the graphs
        x: the arranged positions for the x axis
        y: a list of the concepts that will be represented on the y axis, the items
    in this list must match with an existent global variable and they will match by
    order the axs argument
        width: the width of each bar
        marker: the marker used on the scatter graph
        linewidths: the line widths for drawing the marker
    """

    relative_distances = _get_relative_distances(width, normalized_room_types.keys())

    for idx in range(len(y)):
        for normalized_room_type in normalized_room_types.keys():
            values = globals()[f'_{normalized_room_type}_{y[idx]}']

            axs[idx].scatter(x + relative_distances[normalized_room_type], values, color = color, marker = marker, linewidths = linewidths)

def _plot_lines(neighbourhoods: List[str], normalized_room_types: dict, color: str, axs: List[Axes], x: np.ndarray, y: List[str], width: float):
    """
    Generates line graphs for the user to see based on the
    room types that it receives.

    Arguments:
        neighbourhoods: a list of strings with the neighbourhoods
        normalized_room_types: a dictionary containing the normalized room types
        color: a str representing the color for the graph
        axs: the axes for the graphs
        x: the arranged positions for the x axis
        y: a list of the concepts that will be represented on the y axis, the items
    in this list must match with an existent global variable and they will match by
    order the axs argument
        width: the width of each bar
    """

    relative_distances = _get_relative_distances(width, normalized_room_types.keys())

    for idx in range(len(y)):
        for neighbourhood_idx in range(len(neighbourhoods)):
            locals()[f'{y[idx]}_per_room_type'] = []

            for normalized_room_type in normalized_room_types.keys():
                value = globals()[f'_{normalized_room_type}_{y[idx]}'][neighbourhood_idx]
                locals()[f'{y[idx]}_per_room_type'].append(value)
            
            plot_relative_distances = []
            for relative_distance in relative_distances.values():
                plot_relative_distances.append(x[neighbourhood_idx] + relative_distance)
        
            axs[idx].plot(plot_relative_distances, locals()[f'{y[idx]}_per_room_type'], color = color)

def _get_relative_distances(width: float, bars: List[str]):
    """
    Calculates the distance at which each bar on a bar plot has to be relative
    to the x axis tick given the bars width.

    Arguments:
        width: a float representing the width of each bar
        bars: a list representing the bars for a given x tick
    
    Returns:
        A dictionary containing the distance to the x axis tick for each
    bar
    """

    positions = {}

    if len(bars)%2 == 0:
        start = -0.375 * len(bars)

    else:    
        start = -0.5 * len(bars)

    for idx, current_bar in enumerate(bars):
        positions[current_bar] = (start + idx) * width

    return positions

main()