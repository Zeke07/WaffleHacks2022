import numpy as np
import copy
import heapq
import random
from functools import reduce
from pipe import select, where
from pprint import pprint
from typing import Any, Dict, Iterable, Tuple
DEBUG = False

def nutrition_score(grams: int, rank: int, max_good_rank: int, max_bad_rank: int) -> int:
    """Retrieves single score for a specific nutrition for a food item based on rank."""
    return grams * (max_good_rank - rank + 1 if rank > 0 else max_bad_rank - rank + 1)


def filter_food_item(food_item: Dict[str, Tuple[int, int]]) -> Dict[str, Any]:
    """Filters specific food item by excluding all key-value pairs with non-integer value."""
    name = food_item['name']
    filtered_dict = dict(list(food_item.items()) |
                         where(lambda kvp: type(kvp[1]) in (int, float) or kvp[1].isdigit()) |
                         select(lambda kvp: (kvp[0], int(kvp[1]))))
    filtered_dict = dict(list(filtered_dict.items()) |
                         where(lambda kvp: kvp[1] > 0))
    filtered_dict['name'] = name
    filtered_dict['net score'] = 9
    # pprint(f'filtered_dict:\n{filtered_dict}')
    return filtered_dict


def append_rank_to_food_item(food_item: Dict[str, Any], ranks: Dict[str, int]) -> Dict[str, Any]:
    """Convert each value of user-ranked nutrition to (grams, rank) tuple."""
    food_item_local = copy.deepcopy(x=food_item)
    modified_nutrients = set(food_item.keys()).intersection(set(ranks.keys()))
    # pprint(f'modified_nutrients:\n{modified_nutrients}')
    for ranked_nutrition in modified_nutrients:
        food_item_local[ranked_nutrition] = (food_item[ranked_nutrition], ranks[ranked_nutrition])
    # pprint(f'append_rank_dict:\n{food_item_local}')
    return food_item_local


def append_net_score(food_item: Dict[str, Any]) -> Dict[str, Any]:
    """Find and append net score for a specific food item with its nutritions ranked by preference."""
    # max_good_rank = reduce(lambda x, y: max(x, y[1]) if y[1] > 0 else x, nutrition.values(), 0)
    # max_bad_rank = len(nutrition) - max_good_rank
    food_item_local = copy.deepcopy(x=food_item)
    net_score = sum(food_item.values() |
                    where(lambda x: type(x) == tuple) |
                    select(lambda x: nutrition_score(
                        grams=x[0],
                        rank=x[1],
                        max_good_rank=3,
                        max_bad_rank=3)))
    # print(f'computed score:\t{net_score}')
    food_item_local['net score'] = net_score
    return food_item_local

def transform_food_item(food_item: Dict[str, Any], ranks: Dict[str, int]) -> Dict[str, Any]:
    """Performs all transformations for data cleaning on food items before heapifying."""
    food_item_local = copy.deepcopy(x=food_item)
    food_item_local = filter_food_item(food_item=food_item_local)
    food_item_local = append_rank_to_food_item(food_item=food_item_local, ranks=ranks)
    food_item_local = append_net_score(food_item=food_item_local)
    return food_item_local

# example
if DEBUG:
    ground_beef = dict({
        'name': 'ground_beef',
        'net score': 0,
        'calories': (300, 2),
        'protein': (15, 1),
        'carbohydrates': (25, -2),
        'total fat': (12, -1),
    })

    food_items = list([(''.join(list([chr(letter) for letter in random.choices(population=range(
        ord('a'), ord('z') + 1), k=random.randint(5, 10))])), random.randint(10, 100)) for i in range(10)])
    food_items = list(map(lambda x: (x[0], -x[1]), food_items))
    heapq.heapify(food_items)
    pprint(food_items)

food_items = list([
    {'name': 'Ore-Ida Just Crack an Egg Omelet Rounds Three Meat Egg Bites - 4.6oz', 'price': 3.19, 'Servings Per Container': '1', 'Calories': 270, 'Total Fat': 18, 'Saturated Fat': 9, 'Trans Fat': 0,
        'Cholesterol': 230, 'Sodium': 630, 'Total Carbohydrate': 7, 'Dietary Fiber': 0, 'Sugars': 2, 'Added Sugars': 0, 'Protein': 18, 'Vitamin D': 1.2, 'Calcium': 180, 'Iron': 1.2, 'Potassium': 250},
    {'name': 'All Natural 93/7 Ground Beef - 1lb - Good u0026#38; Gatheru0026#8482;', 'price': 6.69, 'Servings Per Container': '4', 'Calories': 170,
        'Calories From Fat': 70, 'Total Fat': 8, 'Saturated Fat': 3, 'Cholesterol': 65, 'Sodium': 70, 'Total Carbohydrate': 0, 'Protein': 23},
    {'name': 'USDA Choice Angus Beef Stew Meat - 1lb - Good u0026#38; Gatheru0026#8482;', 'price': 7.99, 'Servings Per Container': '3.5', 'Calories': 190,
        'Calories From Fat': 90, 'Total Fat': 10, 'Saturated Fat': 4, 'Cholesterol': 80, 'Sodium': 60, 'Total Carbohydrate': 0, 'Protein': 24},
    {'name': 'USDA Choice Angus Beef Steak Strips - 14oz - Good u0026#38; Gatheru0026#8482;', 'price': 11.99, 'Servings Per Container': '3.5',
        'Calories': 190, 'Calories From Fat': 90, 'Total Fat': 10, 'Saturated Fat': 4, 'Cholesterol': 80, 'Sodium': 60, 'Total Carbohydrate': 0, 'Protein': 24},
    {'name': 'Boneless Center Pork Chops - 15oz - Good u0026#38; Gatheru0026#8482;', 'price': 5.29, 'Servings Per Container': '3', 'Calories': 220,
        'Calories From Fat': 100, 'Total Fat': 11, 'Saturated Fat': 4, 'Cholesterol': 90, 'Sodium': 310, 'Total Carbohydrate': 2, 'Protein': 26},
    {'name': 'Aidells Chicken u0026#38; Apple Smoked Chicken Sausage - 12oz/4ct', 'price': 5.99, 'Servings Per Container': '4', 'Calories': 170, 'Calories From Fat': 100,
        'Total Fat': 11, 'Saturated Fat': 3.5, 'Trans Fat': 0, 'Cholesterol': 75, 'Sodium': 660, 'Total Carbohydrate': 4, 'Dietary Fiber': 1, 'Sugars': 3, 'Protein': 13},
    {'name': 'All Natural 80/20 Ground Beef - 1lb - Good u0026#38; Gatheru0026#8482;', 'price': 5.89, 'Servings Per Container': '4', 'Calories': 280,
        'Calories From Fat': 200, 'Total Fat': 22, 'Saturated Fat': 9, 'Cholesterol': 80, 'Sodium': 75, 'Total Carbohydrate': 0, 'Protein': 19},
    {'name': 'Boneless Thin-Cut Center Cut Pork Chops - 15oz - Good u0026#38; Gatheru0026#8482;', 'price': 5.79, 'Servings Per Container': '5',
        'Calories': 130, 'Calories From Fat': 60, 'Total Fat': 7, 'Saturated Fat': 2.5, 'Cholesterol': 50, 'Sodium': 190, 'Total Carbohydrate': 1, 'Protein': 16},
    {'name': 'Parmesan Chicken Breast Cutlets - 20oz - Good u0026#38; Gatheru0026#8482;', 'price': 11.99, 'Servings Per Container': '4', 'Calories': 320, 'Calories From Fat': 140,
        'Total Fat': 16, 'Saturated Fat': 8, 'Trans Fat': 0, 'Cholesterol': 100, 'Sodium': 320, 'Total Carbohydrate': 9, 'Dietary Fiber': 0, 'Sugars': 0, 'Protein': 33},
    {'name': 'Old Neighborhood Shaved Beef Steak - 14oz', 'price': 6.49, 'Servings Per Container': '7', 'Calories': 100, 'Calories From Fat': 50, 'Total Fat': 6,
        'Saturated Fat': 2, 'Trans Fat': 0, 'Cholesterol': 35, 'Sodium': 40, 'Total Carbohydrate': 0, 'Dietary Fiber': 0, 'Sugars': 0, 'Protein': 11},
    {'name': 'All Natural 85/15 Ground Beef - 1lb - Good u0026#38; Gatheru0026#8482;', 'price': 6.29, 'Servings Per Container': '4', 'Calories': 240,
        'Calories From Fat': 150, 'Total Fat': 17, 'Saturated Fat': 7, 'Cholesterol': 75, 'Sodium': 75, 'Total Carbohydrate': 0, 'Protein': 21},
    {'name': 'Sea Cuisine Pan Sear Teriyaki Sesame Salmon - Frozen - 9oz', 'price': 7.99, 'Servings Per Container': '2', 'Calories': 240, 'Calories From Fat': 110,
        'Total Fat': 12, 'Saturated Fat': 2, 'Trans Fat': 0, 'Cholesterol': 50, 'Sodium': 470, 'Total Carbohydrate': 10, 'Dietary Fiber': 0, 'Sugars': 0, 'Protein': 23},
    {'name': 'Italian Style Beef, Pork, u0026#38; Chicken Meatballs - Frozen - 26oz - Good u0026#38; Gatheru0026#8482;', 'price': 5.39, 'Servings Per Container': 'About 9', 'Calories': 240, 'Total Fat': 20, 'Saturated Fat': 7,
        'Trans Fat': 1, 'Cholesterol': 55, 'Sodium': 590, 'Total Carbohydrate': 5, 'Dietary Fiber': 1, 'Sugars': 1, 'Added Sugars': 1, 'Protein': 11, 'Vitamin D': 0.2, 'Calcium': 40, 'Iron': 1.2, 'Potassium': 280},
    {'name': 'All Natural Chicken Wings - Frozen - 3lbs - Good u0026#38; Gatheru0026#8482;', 'price': 10.69, 'Servings Per Container': 'ABOUT 6', 'Calories': 200, 'Total Fat': 15, 'Saturated Fat': 4,
        'Trans Fat': 0, 'Cholesterol': 110, 'Sodium': 270, 'Total Carbohydrate': 0, 'Dietary Fiber': 0, 'Sugars': 0, 'Added Sugars': 0, 'Protein': 17, 'Potassium': 180, 'Vitamin D': 0, 'Calcium': 0, 'Iron': 0.4},
    {'name': 'Ground Pork - 1lb - Good u0026#38; Gatheru0026#8482;', 'price': 3.49, 'Servings Per Container': '4', 'Calories': 280,
        'Calories From Fat': 200, 'Total Fat': 22, 'Saturated Fat': 8, 'Cholesterol': 70, 'Sodium': 240, 'Total Carbohydrate': 2, 'Protein': 17},
    {'name': "Jack Daniel's Seasoned And Cooked Pulled Pork - 16oz", 'price': 8.99, 'Servings Per Container': 'ABOUT 3', 'Calories': 370, 'Calories From Fat': 180,
        'Total Fat': 20, 'Saturated Fat': 7, 'Trans Fat': 0, 'Cholesterol': 75, 'Sodium': 750, 'Total Carbohydrate': 28, 'Dietary Fiber': 0, 'Sugars': 25, 'Protein': 19},
    {'name': 'Oven Roasted Turkey Breast Ultra-Thin Deli Slices - 9oz - Good u0026#38; Gatheru0026#8482;', 'price': 3.69, 'Servings Per Container': '4.5', 'Calories': 50,
        'Calories From Fat': 10, 'Total Fat': 1, 'Saturated Fat': 0, 'Trans Fat': 0, 'Cholesterol': 10, 'Sodium': 530, 'Total Carbohydrate': 2, 'Dietary Fiber': 0, 'Sugars': 1, 'Protein': 9},
    {'name': 'Ball Park Uncured Beef Franks - 15oz/8ct', 'price': 4.59, 'Servings Per Container': '8', 'Calories': 170, 'Calories From Fat': 130, 'Total Fat': 15,
        'Saturated Fat': 6, 'Trans Fat': 0.5, 'Cholesterol': 30, 'Sodium': 480, 'Potassium': 270, 'Total Carbohydrate': 4, 'Dietary Fiber': 0, 'Sugars': 1, 'Protein': 6},
    {'name': 'Steakhouse Seasoned Tavern Beef Patties - 1.33lbs - Good u0026#38; Gatheru0026#8482;', 'price': 6.99, 'Servings Per Container': '4', 'Calories': 390,
        'Calories From Fat': 270, 'Total Fat': 30, 'Saturated Fat': 12, 'Cholesterol': 95, 'Sodium': 590, 'Total Carbohydrate': 2, 'Sugars': 1, 'Protein': 26},
    {'name': 'Aidells Chicken u0026#38; Apple Smoked Chicken Sausage - 12oz/4ct', 'price': 5.99, 'Servings Per Container': '4', 'Calories': 170, 'Calories From Fat': 100,
        'Total Fat': 11, 'Saturated Fat': 3.5, 'Trans Fat': 0, 'Cholesterol': 75, 'Sodium': 660, 'Total Carbohydrate': 4, 'Dietary Fiber': 1, 'Sugars': 3, 'Protein': 13},
    {'name': 'USDA Choice Angus Beef Stew Meat - 24oz - Good u0026#38; Gatheru0026#8482;', 'price': 10.99, 'Servings Per Container': '7.5', 'Calories': 200, 'Calories From Fat': 110, 'Total Fat': 12, 'Saturated Fat': 5, 'Cholesterol': 60, 'Sodium': 290, 'Total Carbohydrate': 2, 'Protein': 21}, 
    ])

pprint('-' * 100)
pprint(f'food_items:\n{food_items}')

ranks = dict({
    'Protein': 1,
    'Dietary Fiber': 2,
    'Potassium': 3,
    'Cholesterol': -1,
    'Total Fat': -2,
    'Sugar': -3,
})
food_items_transformed = list([transform_food_item(food_item=food_item, ranks=ranks) for food_item in food_items])
heap_items = list(food_items_transformed | select(lambda x: (x['name'], -x['net score'])))

pprint('-' * 100)
pprint(f'food_items_transformed:\n{food_items_transformed}')

heapq.heapify(heap_items)
pprint('-' * 100)
pprint(f'heap_items:\n{heap_items}')

top_of_heap = heapq.heappop(heap_items)
pprint('-' * 100)
print(f'top_of_heap:\n{top_of_heap[0]}')
