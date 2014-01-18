from app import db, Book
import pickle
from amazon import get_amazon_info, get_amazon_image, get_chegg_info, get_amazon_price
import time

def add_book(isbn, course, amz_info, amz_image):
    # on the rare occasion amazon doesn't have a book
    if isinstance(amz_info, basestring):
        amz_info = get_chegg_info(isbn)
        print 'chegged'

    # if chegg also doesn't have it, have to manually update
    if isinstance(amz_info, basestring):
        amz_info = {'url': None,
                    'title': None,
                    'authors': None}
        print 'not in chegg either'

    authors = amz_info['authors']

    if authors is not None:
        authors = list(set(authors))

    b = Book(isbn=isbn, 
             title=amz_info['title'],
             author=authors,
             amazon_url=amz_info['url'],
             image=amz_image,
             courses=[course])
    db.session.add(b)
    db.session.commit()

isbns = pickle.load(open('isbn.p','rb'))

# a list of tuples of only courses that have books
c = []
for course in isbns:
    if course['isbns'] != []:
        c.append(course)

# remove all invalid isbns; I believe the invalid ones are brown bookstore lab packets etc.
clean = []
for course in c:
    i = []
    for isbn in course['isbns']:
        if isbn.isdigit():
            i.append(isbn)
    clean.append({'id': course['id'], 'isbns': list(set(i))})
"""
# populate database
while True:
    try:
        for course in clean:
            for isbn in course['isbns']:
                exists = Book.query.get(int(isbn))
                if exists != None:
                    if course['id'] not in exists.courses:
                        temp = list(exists.courses)
                        temp.append(course['id'])
                        exists.courses = temp
                        db.session.commit()
                        print course['id'] + " " + str(isbn)
                    print '%s exists'%(isbn)
                else:
                    info = get_amazon_info(isbn)
                    time.sleep(1)
                    img = get_amazon_image(isbn)
                    add_book(int(isbn), course['id'], info, img)
                    print 'added: ' + isbn
                    time.sleep(1)
    except:
        print "restarting"
        continue
    break
"""
"""
# add price values
books = Book.query.filter(Book.amazon_url != None)

while True:
    try:
        for book in books:
            if book.amazon_price is None:
                book.amazon_price = get_amazon_price(book.isbn)
                time.sleep(1)
                db.session.commit()
                print book.amazon_price
    except:
        print "restarting"
        continue
    break

"""
