import requests
import datetime
from bs4 import BeautifulSoup


def dilbert():
    dilbert_url = 'http://dilbert.com/'
    today_url = dilbert_url + str(datetime.datetime.now().date())
    page_dilbert = requests.get(today_url)
    if page_dilbert.ok:
        soup = BeautifulSoup(page_dilbert.content, 'html.parser')
        url_img = soup.find_all('div', {'class': ['img-comic-container']})[0].find('img')['src']
    else:
        url_img = 'blablaplaceholder'
    return url_img


def xkcd():
    xkcd_url = 'https://xkcd.com/'
    page_xkcd = requests.get(xkcd_url)
    if page_xkcd.ok:
        soup_xkcd = BeautifulSoup(page_xkcd.content, 'html.parser')
        url_img_xkcd = 'http:' + soup_xkcd.findAll('div', {'id': 'comic'})[0].findAll('img')[0]['src']
    else:
        url_img_xkcd = 'blablaplaceholder'
    return url_img_xkcd


def calvin():
    calvin_url = 'https://www.gocomics.com/calvinandhobbes/'+ ('/').join(str(datetime.datetime.now().date()).split('-'))
    page_calvin = requests.get(calvin_url)
    if page_calvin.ok:
        soup_calvin = BeautifulSoup(page_calvin.content, 'html.parser')
        url_calvin = soup_calvin.find('meta', property="og:image").get("content")
    else:
        url_calvin = 'blablaplaceholder'
    return url_calvin


def phd():
    phd_url = 'http://phdcomics.com/comics'
    page_phd = requests.get(phd_url)
    if page_phd.ok:
        soup_phd = BeautifulSoup(page_phd.content, 'html.parser')
        url_phd = soup_phd.find('meta', property="og:image").get("content")
    else:
        url_phd = 'blablaplaceholder'
    return url_phd
