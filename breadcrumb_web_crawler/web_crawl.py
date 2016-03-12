import csv
import os

from bs4 import BeautifulSoup
import requests
import requests.exceptions
from collections import deque
import re
from urlparse import urlsplit
import click


class Site:
    def __init__(self, name, url, category, sub_dirs=False, limit=10):
        self.name = name
        self.url = url
        self.category = category
        self.emails = set()
        self.scraped = False
        self.sub_dirs = sub_dirs
        self.limit = limit

    def get_csv(self):
        csv_str = ''
        for email in self.emails:
            row = '{},{},{},{}\n'.format(self.category, self.name, self.url, email)
            csv_str += row
        return csv_str

    def scrape_emails(self):
        self.scraped = True
        new_urls = deque([self.url])
        # a set of urls that we have already crawled
        processed_urls = set()
        count = 0
        while len(new_urls):
            # move next url from the queue to the set of processed urls
            url = new_urls.popleft()
            processed_urls.add(url)

            # extract base url to resolve relative links
            parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/') + 1] if '/' in parts.path else url

            if parts.path.split('.')[len(parts.path.split('.')) - 1] == 'pdf':
                continue
            # get url's content

            try:
                response = requests.get(url, timeout=1.0)
            except Exception, e:
                print e
                continue
            # extract all email addresses and add them into the resulting set
            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
            try:
                print "Found {} emails in {} with a total of {} emails in this domain.".format(len(new_emails), url,
                                                                                               len(self.emails))
            except Exception, e:
                print e
            self.emails.update(new_emails)

            # create a beutiful soup for the html document
            soup = BeautifulSoup(response.text)

            # find and process all the anchors in the document
            for anchor in soup.find_all("a"):
                count+=1
                # extract link url from the anchor
                link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                # resolve relative links
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                # add the new url to the queue if it was not enqueued nor processed yet
                if not link in new_urls and not link in processed_urls:
                    if self.sub_dirs:
                        if count <= self.limit:
                            new_urls.append(link)


@click.command()
@click.option('--sites', '-s', default='sites.csv', help='Input csv file.')
@click.option('--outfile', '-o', default='sites_emails.csv', help='Output csv file.')
@click.option('--limit', '-l', default=10, help='Limit number of sub urls to visit.')
@click.option('--sub_dirs', '-sd', is_flag=True, default=False, help='Output csv file.')
def crawl(sites='sites.csv', outfile='sites_emails.csv', sub_dirs=False, limit=10):
    if not os.path.isfile(sites):
        print 'File {} does not exist.'.format(sites)
        return

    with open(sites) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category = row['category']
            name = row['name']
            url = row['url']

            site = Site(url=url, name=name, category=category, sub_dirs=sub_dirs, limit=limit)
            site.scrape_emails()
            data = site.get_csv()

            with open(outfile, "a") as myfile:
                myfile.write(data)

            print site.get_csv()


if __name__ == '__main__':
    crawl()
