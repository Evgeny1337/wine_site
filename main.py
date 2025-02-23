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


def get_wine_data(wines_file):
    wine_data_df = pandas.read_excel(wines_file,
                                     sheet_name='Лист1').fillna('')
    wine_records = wine_data_df.to_dict(orient='records')
    wine_info = collections.defaultdict(str)
    for row in wine_records:
        wine = {
            'image': os.path.join('images', row.get('Картинка', '')),
            'name': row.get('Название', ''),
            'sort': row.get('Сорт', ''),
            'price': str(row.get('Цена', '')),
            'promo': str(row.get('Акция', '')),
            'disabled_sort': True if row['Категория'] in DISABLED_SORT
            else False
        }
        wine_info.setdefault(row['Категория'], []).append(wine)
    return wine_info


def main():
    load_dotenv()
    wines_file = os.environ['WINES_FILE']
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    wines_collection = get_wine_data(wines_file)

    year_count = datetime.datetime.now().year - FOUNDING_DATE
    template = env.get_template('template.html')

    rendered_page = template.render(
        wines_collection=wines_collection,
        year=get_years_with_correct_declension(year_count)
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
