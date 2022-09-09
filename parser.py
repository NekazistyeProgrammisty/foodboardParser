import requests
from bs4 import BeautifulSoup
import json

Unique_products = {"null_rpoduct": 0}
JSON_products = []

Unique_categories = {"bull_category": 0}
JSON_categories = []

JSON_recipes = []

def parse_recipe_products(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='html.parser')
    ingredients = soup.find_all('span', {'itemprop': 'recipeIngredient'})
    for ingredient in ingredients:
        ingr = ingredient.text
        if ingr not in Unique_products:
            Unique_products[ingr] = len(Unique_products)
            JSON_products.append({"id": len(JSON_products)+1, "name": ingr})


def parse_recipe_categories(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='html.parser')
    categories = soup.find('div', {"itemtype": "http://schema.org/BreadcrumbList"})
    if categories is not None:
        categories = categories.find_all('span', {"class": "emotion-yq9yyo"})
        for category in categories:
            cat = category.text
            if cat != "" and cat != "главная" and cat not in Unique_categories:
                Unique_categories[cat] = len(Unique_categories)
                JSON_categories.append({"id": len(JSON_categories), "name": cat})



def parse_recipe_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='html.parser')

    title = soup.find('div', {'class': 'emotion-1h7uuyv'}).find('h1').text
    description = soup.find('span', {'class': 'emotion-1x1q7i2'})
    if description is not None:
      description = description.text
    img = soup.find('img', {'class': ' emotion-1sh0a0t'})['src']

    products = []
    ingredients = soup.find_all('span', {'itemprop': 'recipeIngredient'})
    for ingredient in ingredients:
        ingr = ingredient.text
        products.append(Unique_products[ingr])
    product_count = len(products)

    categories = []
    cats_list = soup.find('div', {"itemtype": "http://schema.org/BreadcrumbList"})
    if cats_list is not None:
        cats_list = cats_list.find_all('span', {"class": "emotion-yq9yyo"})
        for category in cats_list:    
            cat = category.text
            if cat != "" and cat != "главная":
                categories.append(Unique_categories[cat])

    recipe = {
        "id": len(JSON_recipes),
        "title": title,
        "description": description,
        "main_image": img,
        "total_products_count": product_count,
        "included_products": products,
        "recipe_category": categories
    }
    JSON_recipes.append(recipe)


def parse_page():
    PAGES_ROOT = "https://eda.ru/recepty?page="
    ROOT = "https://eda.ru"
    i = 1
    page = True

    while page is not None and i < 2: # 715:
        url = PAGES_ROOT + str(i)
        print(url)
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, features='html.parser')
            recipes = soup.find_all('div', {'class': 'emotion-m0u77r'})
            for recipe in recipes:
                recipe_url = ROOT + recipe.find('a')['href']
                print(recipe_url)
                parse_recipe_products(recipe_url)
                parse_recipe_categories(recipe_url)
                parse_recipe_data(recipe_url)
        except:
            print("ERROR HERE!!!")
        i += 1


parse_page()
with open('products.json', 'w') as f1:
    json.dump(JSON_products, f1, indent=4, ensure_ascii=False)
with open('categories.json', 'w') as f2:
    json.dump(JSON_categories, f2, indent=4, ensure_ascii=False)
with open('recipes.json', 'w') as f3:
    json.dump(JSON_recipes, f3, indent=4, ensure_ascii=False)