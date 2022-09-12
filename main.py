#from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from collections import defaultdict

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

excel_data_df = pandas.read_excel(io="wine3.xlsx", na_values='nan', keep_default_na=False)
categories = excel_data_df['Категория'].unique()
wine_categories = defaultdict(list)
wines_description = excel_data_df.to_dict(orient="records")
for category in categories:
    for wine in wines_description:
        if category == wine['Категория']:
            wine_categories[category].append(wine)


def calculate_year():
    start_year = 1920
    current_year = datetime.datetime.today().year
    return current_year - start_year


def agree_year_and_noun():
    year = calculate_year()
    remainder = year % 100
    if remainder == 0 or remainder in range(5, 21):
        return "лет"
    elif remainder == 1:
        return "год"
    else:
        return "года"


rendered_page = template.render(age=calculate_year(), year=agree_year_and_noun(), wine_categories=wine_categories)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)


#server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
#server.serve_forever()