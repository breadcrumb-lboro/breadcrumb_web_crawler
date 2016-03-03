import requests
from bs4 import BeautifulSoup
import time
YELL_ROOT = "https://www.yell.com/ucs/UcsSearchAction.do?keywords={}&location={}&pageNum={}"
YELP_ROOT = "http://www.yelp.com/search?find_desc={}&find_loc={}"
PAGE_LIMIT = 1


def grab_content(cat, location="London", page=1):
    url = YELL_ROOT.format(cat, location, page)
    content = requests.get(url)
    return content.content


def crawl():
    categories = ['Mechanic', 'Salon']

    for cat in categories:
        for page_no in range(1, PAGE_LIMIT + 1):
            html = grab_content(cat, page=page_no)
            soup = BeautifulSoup(html, 'html.parser')
            print soup.contents
            time.sleep(1)

            content = soup.find_all("div", class_="row")
            print content


if __name__ == '__main__':
    crawl()
