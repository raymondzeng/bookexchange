# searching amazon books by ISBN
# for exmaple, my chinese textbook's ISBN is 0691153108
# and below is the code to find it's amazon url, title, and authors

from bs4 import BeautifulSoup
import bottlenose

amazon = bottlenose.Amazon("AKIAJU37EOGXIYUI4HMA","Dh3ngz4QHf5xKw2tQFj+/LJhJEuExsF1hmt9qZAL","1")

# ItemId is the ISBN
# response is in XML
response = amazon.ItemLookup(ItemId="0691153108", ResponseGroup="ItemAttributes", SearchIndex="Books",IdType="ISBN")

soup = BeautifulSoup(response)

# prints the xml in a readable format
# print(soup.prettify())

# gets the url on amazon where the book is located
url = soup.detailpageurl.string

# the title that corresponds to the ISBN
title = soup.title.string

# a list of string of the authors of the book
authors = map(lambda x: x.get_text(), soup.find_all("author"))


print url 
print
print title
print
print authors

# the response has a bunch of other data that we probably don't need but feel free to print out the prettified xml and look at it
