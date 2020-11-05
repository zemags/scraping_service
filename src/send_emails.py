import os, sys
from collections import defaultdict
import datetime

from django.core.mail import EmailMultiAlternatives

#  without runserver by django we can start particularly to save data to DB
from django.contrib.auth import get_user_model
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
import django
django.setup()
#

from scraping.models import Vacancy, Error, URL, Url
from scraping_service.settings import EMAIL_HOST_USER

ADMIN_USER = ''
User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')  # get all values from db
empty = '<h2>No vacancies</h2>'
today = datetime.date.today()

users_dict = {}
if qs.exists():
    params = defaultdict(list)
    vacancies = defaultdict(list)
    for query in qs:
        users_dict[(query['city'], query['language'])] = [query['email']]
        params['city_id__in'].append(query['city'])
        params['language_id__in'].append(query['language'])

    qs_vacancies = Vacancy.objects.filter(**params, timestamp=today).values()
    if qs_vacancies.exists():
        for vacancy in qs_vacancies:
            vacancies[(vacancy['city_id'], vacancy['language_id'])].append(vacancy)
        for keys, emails in users_dict.items():
            rows = vacancies.get(keys, [])
            html = ''
            for row in rows:
                html += '<a href="{url}">{title}</a><br>'.format(url=row['url'], title=row['title'])
            html_ = html if html else empty
            for email in emails:
                msg = EmailMultiAlternatives(
                    subject='Vacancy sender from %s' % today,
                    body='Vacancy sender',
                    from_email=EMAIL_HOST_USER,
                    to=[email])
                msg.attach_alternative(html_, 'text/html')
                msg.send()

qs = Error.objects.filter(timestamp=today)
if qs.exists():
    error = qs.first()
    data = error.data
    html = ''
    for er in data:
        html += '<a href="{url}">{title}</a><br>'.format(url=er['url'], title=er['title'])
    html_ = html if html else 'No errors'
    msg = EmailMultiAlternatives(
        subject='Errors sender from %s' % today,
        body='Errors sender',
        from_email=EMAIL_HOST_USER,
        to=[ADMIN_USER]
    )
    msg.attach_alternative(html_, 'text/html')
    msg.send()

qs = Url.objects.all().values('city', 'language')
urls_dict = {(i['city'], i['language']): True for i in qs}
urls_err = ''
for keys in users_dict.keys():
    if not urls_dict.get(keys):
        urls_err += 'for {city} and {language} there is no urls<br>'.format(city=keys[0], language=keys[0])
if urls_err:
    msg = EmailMultiAlternatives(
        subject='Urls error sender from %s' % today,
        body='Urls errors sender',
        from_email=EMAIL_HOST_USER,
        to=[ADMIN_USER]
    )
    msg.attach_alternative(html_, 'text/html')
    msg.send()