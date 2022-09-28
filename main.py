from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
from collections import defaultdict
import argparse

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def create_parser():
    """create parser to receive the path to the file"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs='?', default='wine.xlsx', help="path to the file")
    return parser.parse_args()


def agree_year_and_noun():
    """return correct name "год/года/лет"""
    year = calculate_year()
    remainder = year % 100
    if remainder == 0 or remainder in range(5, 21):
        return "лет"
    elif remainder == 1:
        return "год"
    else:
        return "года"


def calculate_year():
    """ receive age """
    start_year = 1920
    current_year = datetime.datetime.today().year
    return current_year - start_year


def receive_wine_by_categories(filepath):
    """receive categories from filepath"""
    wine_categories = defaultdict(list)
    excel_wine_data = pandas.read_excel(
        io=filepath, na_values="nan", keep_default_na=False
    ).to_dict(orient="records")
    for wine in excel_wine_data:
        wine_categories[wine["Категория"]].append(wine)
    return wine_categories


if __name__== "__main__":

    args = create_parser()
    filepath = args.filepath

    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("template.html")

    rendered_page = template.render(
        age=calculate_year(),
        year=agree_year_and_noun(),
        wine_categories=receive_wine_by_categories(filepath)
    )

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
