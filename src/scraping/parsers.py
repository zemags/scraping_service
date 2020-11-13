import codecs

import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

__all__ = ('work', 'dou')

headers  = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


def work(url, city=None, language=None):
    jobs = list()
    errors = list()

    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers={'User-Agent': UserAgent().random})

        if resp.status_code == 200:
            soup = bs(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'job_link'})
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']  # access to attrs
                    content = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({
                        'title': ' '.join(title.text.split()), 'url': '%s%s' % (domain, href), 'description': content, 'company': company,
                        'city_id': city, 'language_id': language
                    })
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def dou(url, city=None, language=None):
    jobs = list()
    errors = list()
    if url:
        resp = requests.get(url, headers={'User-Agent': UserAgent().random})

        if resp.status_code == 200:
            soup = bs(resp.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')
            if main_div:
                li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_list:
                    title = li.find('div', attrs={'class': 'title'})
                    href = title.a['href']  # access to attrs
                    cont = li.find('div', attrs={'class': 'sh-info'})
                    content = cont.text
                    company = 'No name'
                    a = title.find('a', attrs={'class', 'company'})
                    if a:
                        company = a.text
                    jobs.append({'title': ' '.join(title.text.split()), 'url': href, 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language
                    })
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors
