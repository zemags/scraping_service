import os, sys
from collections import defaultdict

from django.core.mail import EmailMultiAlternatives

#  without runserver by django we can start particularly to save data to DB
from django.contrib.auth import get_user_model
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
import django
django.setup()
#

from scraping.models import Vacancy
from scraping_service.settings import EMAIL_HOST_USER


User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')  # get all values from db
empty = '<h2>No vacancies</h2>'

if qs.exists():
    users_dict = {}
    params = defaultdict(list)
    vacancies = defaultdict(list)
    for query in qs:
        users_dict[(query['city'], query['language'])] = [query['email']]
        params['city_id__in'].append(query['city'])
        params['language_id__in'].append(query['language'])

    qs_vacancies = Vacancy.objects.filter(**params).values()
    if qs_vacancies.exists():
        for vacancy in qs_vacancies:
            vacancies[(vacancy['city_id'], vacancy['language_id'])].append(vacancy)
        for keys, emails in users_dict.items():
            rows = vacancies.get(keys, [])
            html = ''
            for row in rows:
                html += '<a href="{url}">{title}</a>'.format(url=row['url'], title=row['title'])
            html_ = html if html else empty
            for email in emails:
                msg = EmailMultiAlternatives(
                    subject='Vacancy sender',
                    body='Vacancy sender',
                    from_email=EMAIL_HOST_USER,
                    to=[email])
                msg.attach_alternative(html_, 'text/html')
                msg.send()
