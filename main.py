#from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import  datetime

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


def wine_age():
    start_year = 1920
    current_year = datetime.datetime.today().year
    return current_year - start_year


def correct_year():
    year = wine_age()
    remainder = year % 100
    if remainder == 0 or remainder in range(5, 21):
        return "лет"
    elif remainder == 1:
        return "год"
    else:
        return "года"


rendered_page = template.render(age=wine_age(), year=correct_year())

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

#server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
#server.serve_forever()