import copy

from flask import render_template, Blueprint, request, flash
import main
import algorithm
from pipe import select, where
import heapq
#products=main.create_model("meat", 20.0)
#print(products)

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
        '''
        for item in list:
            if not item:
                flash("required")
                is_loaded=False
        '''
        if not budget:
            flash("Budget is required")
        elif not query:
            flash("Query is required")
        else:
            rankings={nut1: 1, nut2: 2, nut3: 3, nut4:-1, nut5:-2, nut6:-3}
            result=main.create_model(query, budget)
            print(result)
            food_items_transformed=[]
            #food_items_transformed = list([transform_food_item(food_item=food_item, ranks=rankings) for food_item in result])
            for food_item in result:
                food_item_local = copy.deepcopy(x=food_item)
                food_item_local = algorithm.filter_food_item(food_item=food_item_local)
                food_item_local = algorithm.append_rank_to_food_item(food_item=food_item_local, ranks=rankings)
                food_item_local= algorithm.append_net_score(food_item=food_item_local)
                food_items_transformed.append(food_item_local)

            #print(food_items_transformed)
            #heap_items = list(food_items_transformed | select(lambda x: (x['name'], -x['net score'])))
            output=max(food_items_transformed, key=lambda x: x['net score'])
            print(output)



    return render_template("index.html")