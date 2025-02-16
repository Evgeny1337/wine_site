from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime


def years_with_correct_declension(years):
    if years % 10 == 1 and years % 100 != 11:
        return f"{years} год"
    elif 2 <= years % 10 <= 4 and not (12 <= years % 100 <= 14):
        return f"{years} года"
    return f"{years} лет"


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

wines = [
    {
        'image': 'images/izabella.png',
        'name': 'Изабелла',
        'sort': 'Изабелла',
        'price': '350'
    },
    {
        'image': 'images/granatovyi_braslet.png',
        'name': 'Гранатовый браслет',
        'sort': 'Мускат розовый',
        'price': '350'
    },
    {
        'image': 'images/shardone.png',
        'name': 'Шардоне',
        'sort': 'Шардоне',
        'price': '350'
    },
    {
        'image': 'images/belaya_ledi.png',
        'name': 'Дамский пальчик',
        'sort': 'Дамский пальчик',
        'price': '399'
    },
    {
        'image': 'images/rkaciteli.png',
        'name': 'Ркацители',
        'sort': 'Ркацители',
        'price': '499'
    },
    {
        'image': 'images/hvanchkara.png',
        'name': 'Хванчкара',
        'sort': 'Александраули',
        'price': '550'
    },

]


year_count = datetime.datetime.now().year - 1920
template = env.get_template('template.html')

rendered_page = template.render(
    wines=wines, year=years_with_correct_declension(year_count))

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
