# searching amazon books by ISBN
# for exmaple, my chinese textbook's ISBN is 0691153108
# and below is the code to find it's amazon url, title, and authors

import os
from bs4 import BeautifulSoup
import bottlenose
import urllib2
from decimal import Decimal
s3_key = os.environ['S3_KEY']
s3_secret = os.environ['S3_SECRET']

amazon = bottlenose.Amazon(s3_key,s3_secret,"1")

# ItemId is the ISBN, can be both ISBN10 and ISBN13
# response is in XML

def get_amazon_info(isbn):
    response = amazon.ItemLookup(ItemId= str(isbn), ResponseGroup="ItemAttributes", SearchIndex="Books",IdType="ISBN")
    soup = BeautifulSoup(response)
    error = soup.message
    if error is None:
        info = {'url': soup.detailpageurl.string,
                'title': soup.title.string, 
                'authors': map(lambda x: x.get_text(), soup.find_all("author"))}
        return info
    else:
        return error.string

def get_amazon_price(isbn):
    response = amazon.ItemLookup(ItemId= str(isbn), ResponseGroup="ItemAttributes", SearchIndex="Books",IdType="ISBN")
    soup = BeautifulSoup(response)
    price = soup.formattedprice
    if price is not None:
        return Decimal(soup.formattedprice.string[1:])
    else:
        return None

def get_amazon_image(isbn):
    response = amazon.ItemLookup(ItemId= str(isbn), ResponseGroup="Images", SearchIndex="Books",IdType="ISBN")
    soup = BeautifulSoup(response)
    if soup.largeimage is None:
        return "error"
    else:
        return soup.largeimage.url.string

def get_chegg_info(isbn):
    response = urllib2.urlopen('http://www.chegg.com/search/' + str(isbn))
    soup = BeautifulSoup(response)

    authors = soup.find_all('div', class_='author-container')
    if authors == []:
        return "not on chegg"
    author = authors[0].a
    if author is None:
        author = None
    else:
        author = author.string

    title = soup.find_all('div', class_='book-title-container')[0].span.span.string
    info = {'url': None,
            'title': title,
            'authors': [author]}
    return info
