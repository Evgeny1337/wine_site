from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import os
from dotenv import load_dotenv

DISABLED_SORT = ['Напитки']
FOUNDING_DATE = 1920


def get_years_with_correct_declension(years):
    if years % 10 == 1 and years % 100 != 11:
        return f"{years} год"
    elif 2 <= years % 10 <= 4 and not (12 <= years % 100 <= 14):
        return f"{years} года"
    return f"{years} лет"


def get_fill_wines_data(wines_file):
    excel_data = pandas.read_excel(wines_file,
                                   sheet_name='Лист1').fillna('')
    data = excel_data.to_dict(orient='records')
    wines_data = collections.defaultdict(str)
    for row in data:
        wine = {
            'image': os.path.join('images', row.get('Картинка', '')),
            'name': row.get('Название', ''),
            'sort': row.get('Сорт', ''),
            'price': str(row.get('Цена', '')),
            'promo': str(row.get('Акция', '')),
            'disabled_sort': True if row['Категория'] in DISABLED_SORT
            else False
        }
        wines_data.setdefault(row['Категория'], []).append(wine)
    return wines_data


def main():
    load_dotenv()
    wines_file = os.environ['WINES_FILE']
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    # Исправить wine_list
    wine_list = get_fill_wines_data(wines_file)

    year_count = datetime.datetime.now().year - FOUNDING_DATE
    template = env.get_template('template.html')

    rendered_page = template.render(
        wine_list=wine_list, year=get_years_with_correct_declension(year_count))

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
