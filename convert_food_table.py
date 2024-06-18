# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 19:03:46 2024

This script will convert the Norwegian "Matvaretabellen" given as a json file
to a json file compatible with the open source calorie tracker app waistline.

@author: Daniel Alexander Philipps
"""

import json


if __name__ == '__main__':
    # parameters
    input_file_name = 'foods.json'
    output_file_name = 'foods_converted.json'
    
    # Equivalence table for matching nutrients
    nutrient_equivalents = {'calcium': 'Ca',
                            'carbohydrates': 'Karbo',
                            'cholesterol': 'Kolest',
                            'fat': 'Fett',
                            'fiber': 'Fiber',
                            'iron': 'Fe',
                            'proteins': 'Protein',
                            'saturated-fat': 'Mettet',
                            'sodium': 'Na',
                            'sugars': 'Sukker',
                            'trans-fat': 'Trans',
                            'vitamin-a': 'Vit A',
                            'vitamin-c': 'Vit C'}  
    
    
    # import data
    with open(input_file_name, 'r') as data_file:
        file_txt = data_file.read()
        data_file.close()
        del data_file
        
    foods = json.loads(file_txt)['foods']
    
    
    # # for seeing, what the target dict structure should look like.
    # # template import
    # with open('template.json', 'r') as template_file:
    #     file_txt = template_file.read()
    #     template_file.close()
    #     del template_file
        
    # template = json.loads(file_txt)
    
    
    # convert data
    data_converted = dict()
    data_converted['version'] = 1
    food_list = list()
    
    for food in foods:
        if len(food['portions']) > 0: # skip foods without portion size
            food_converted = dict()
            # basic parameters
            food_converted['name'] = food['foodName']
            food_converted['uniqueId'] = food['foodId']
            food_converted['brand'] = 'None'
            food_converted['portion'] = food['portions'][0]['quantity']
            food_converted['unit'] = food['portions'][0]['unit']
            # nutrients
            food_converted['nutrition'] = dict()
            food_converted['nutrition']['calories'] = food['calories']['quantity']
            nutrients_dict = dict()
            for nutrient in food['constituents']:
                nutrients_dict[nutrient['nutrientId']] = nutrient
            # test for quantity field in nutrients
            for nutrient in nutrient_equivalents.keys():
                if 'quantity' in nutrients_dict[nutrient_equivalents[nutrient]].keys():
                    food_converted['nutrition'][nutrient] = \
                        nutrients_dict[nutrient_equivalents[nutrient]]['quantity']
            food_list.append(food_converted)
    
    data_converted['foodList'] = food_list
    data_converted_txt = json.dumps(data_converted)
    
    with open(output_file_name, 'w+') as file:
        file.write(data_converted_txt)
        file.close()
