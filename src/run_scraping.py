import asyncio
import os, sys
import datetime

#  without runserver by django we can start particularly to save data to DB
from django.contrib.auth import get_user_model
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
import django
django.setup()
#
from django.db import DatabaseError


from scraping.parsers import *
from scraping.models import Vacancy, Error, Url

User = get_user_model()
parsers = ((work, 'work'), (dou, 'dou'))
jobs, errors = [], []

def get_settings():
    # get pair city language like id
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst

def get_ursl(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if url_dict[pair]:
            tmp = {'city': pair[0], 'language': pair[1], 'url_data': url_dict[pair]}
            urls.append(tmp)
    return urls

#async variation
async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_ursl(settings)

loop = asyncio.get_event_loop()
tmp_tasks = [
    (func, data['url_data'][key], data['city'], data['language'])
    for data in url_list
    for func, key in parsers
]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

#synchronize variation
# for data in url_list:
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=datetime.date.today())
    if qs.exists():
        # check if error already exists in db
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors: {errors}').save()
