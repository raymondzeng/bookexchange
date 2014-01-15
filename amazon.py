# searching amazon books by ISBN
# for exmaple, my chinese textbook's ISBN is 0691153108
# and below is the code to find it's amazon url, title, and authors

from bs4 import BeautifulSoup
import bottlenose

amazon = bottlenose.Amazon("AKIAJU37EOGXIYUI4HMA","Dh3ngz4QHf5xKw2tQFj+/LJhJEuExsF1hmt9qZAL","1")

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

def get_amazon_image(isbn):
    response = amazon.ItemLookup(ItemId= str(isbn), ResponseGroup="Images", SearchIndex="Books",IdType="ISBN")
    soup = BeautifulSoup(response)
    error = soup.message
    if error is None:
        return soup.largeimage.url.string
    else:
        return error.string

#print get_amazon_info('9780691153100')
