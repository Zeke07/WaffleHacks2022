'''
Base application for Flask communication with app webpage
Version Date: 6-19-2022
'''

import copy

from flask import render_template, Blueprint, request, flash
import main
import algorithm

views = Blueprint(__name__,'views')

@views.route("/", methods=("GET","POST"))
def home():

    if request.method=="POST":
        budget=request.form["budget"]
        query=request.form["query"]
        nut1=request.form['thing1']
        nut2=request.form['thing2']
        nut3=request.form['thing3']
        nut4=request.form['thing4']
        nut5=request.form['thing5']
        nut6=request.form['thing6']
        list=[nut1,nut2,nut3,nut4,nut5,nut6]

        if not budget:
            flash("Budget is required")
        elif not query:
            flash("Query is required")
        else:

            rankings={nut1: 1, nut2: 2, nut3: 3, nut4:-1, nut5:-2, nut6:-3}
            result=main.create_model(query, budget)
            food_items_transformed=[]

            for food_item in result:
                food_item_local = copy.deepcopy(x=food_item)
                food_item_local = algorithm.filter_food_item(food_item=food_item_local)
                food_item_local = algorithm.append_rank_to_food_item(food_item=food_item_local, ranks=rankings)
                food_item_local= algorithm.append_net_score(food_item=food_item_local)
                food_items_transformed.append(food_item_local)

            output=max(food_items_transformed, key=lambda x: x['net score'])

            original_dictionary = {}
            for iterator in result:
                if (iterator['name'] == output['name']):
                    original_dictionary = iterator
            name=original_dictionary.pop('name')
            price=original_dictionary.pop('price')
            link=original_dictionary.pop('link')
            difference= float(budget)- float(price)
            curr = {"Protein": 0, "Total Carbohydrate": 0, "Total Fat": 0, "Dietary Fiber": 0, "Saturated Fat": 0,
                    "Trans Fat": 0, "Cholesterol": 0, "Sodium": 0, "Sugars": 0}
            for item in curr:
                if item in original_dictionary.keys():
                    curr[item]=original_dictionary[item]
            return render_template("index.html", name=name, price=price, difference=difference, link=link, protein=f'Protein: {curr["Protein"]}', carbs=f'Carbs: {curr["Total Carbohydrate"]}', fats=f'Fats: {curr["Total Fat"]}', fiber=f'Fiber: {curr["Dietary Fiber"]}', sat=f'Saturated Fat: {curr["Saturated Fat"]}', trans=f'Trans Fat: {curr["Trans Fat"]}', cholesterol=f'Cholesterol: {curr["Cholesterol"]}', sodium=f'Sodium: {curr["Sodium"]}', sugar=f'Sugar: {curr["Sugars"]}')




    else:
        return render_template("index.html")
