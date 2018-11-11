import requests
import datetime
from bs4 import BeautifulSoup


def dilbert():
    dilbert_url = 'http://dilbert.com/'
    today_url = dilbert_url + str(datetime.datetime.now().date())
    page = requests.get(today_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    url_img = soup.find_all('div', {'class': ['img-comic-container']})[0].find('img')['src']
    return url_img


def xkcd():
    xkcd_url = 'https://xkcd.com/'
    page_xkcd = requests.get(xkcd_url)
    soup_xkcd = BeautifulSoup(page_xkcd.content, 'html.parser')
    url_img_xkcd = 'http:' + soup_xkcd.findAll('div', {'id': 'comic'})[0].findAll('img')[0]['src']
    return url_img_xkcd


def calvin():
    calvin_url = 'https://www.gocomics.com/calvinandhobbes/'+ ('/').join(str(datetime.datetime.now().date()).split('-'))
    page_calvin = requests.get(calvin_url)
    soup_calvin = BeautifulSoup(page_calvin.content, 'html.parser')
    url_calvin = soup_calvin.find('meta', property="og:image").get("content")
    return url_calvin


def phd():
    phd_url = 'http://phdcomics.com/comics'
    page_phd = requests.get(phd_url)
    soup_phd = BeautifulSoup(page_phd.content, 'html.parser')
    url_phd = soup_phd.find('meta', property="og:image").get("content")
    return url_phd
