from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import os


def years_with_correct_declension(years):
    if years % 10 == 1 and years % 100 != 11:
        return f"{years} год"
    elif 2 <= years % 10 <= 4 and not (12 <= years % 100 <= 14):
        return f"{years} года"
    return f"{years} лет"


def get_fill_data_from_excel():
    excel_data = pandas.read_excel('wine2.xlsx',
                                   sheet_name='Лист1').fillna('')
    excel_list = excel_data.to_dict(orient='records')
    wine_list = collections.defaultdict(str)
    for row in excel_list:
        wine = {
            'image': os.path.join('images', row.get('Картинка', '')),
            'name': row.get('Название', ''),
            'sort': row.get('Сорт', ''),
            'price': str(row.get('Цена', ''))
        }
        wine_list.setdefault(row['Категория'], []).append(wine)
    return wine_list


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

wine_list = get_fill_data_from_excel()

year_count = datetime.datetime.now().year - 1920
template = env.get_template('template.html')

rendered_page = template.render(
    wine_list=wine_list, year=years_with_correct_declension(year_count))

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
