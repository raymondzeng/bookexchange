from app import db, Book
import pickle
from amazon import get_amazon_info, get_amazon_image, get_chegg_info
import time

def add_book(isbn, course, amz_info, amz_image):
    # on the rare occasion amazon doesn't have a book
    if isinstance(amz_info, basestring):
        amz_info = get_chegg_info(isbn)
        print 'chegged'
    # if chegg also doesn't have it, have to manually fill
    if isinstance(amz_info, basestring):
        amz_info = {'url': None,
                    'title': None,
                    'authors': [None]}
        print 'not in chegg either'
    authors = amz_info['authors']
    author = ""
    if authors is not None and authors != []:
        if authors[0] is not None:
            for a in authors:
                author = author + "," + a

    b = Book(isbn=isbn, 
             title=amz_info['title'],
             author=author,
             amazon_url=amz_info['url'],
             image=amz_image,
             courses=course)
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
    clean.append({'id': course['id'], 'isbns': i})

for course in clean:
    for isbn in course['isbns']:
        exists = Book.query.filter_by(isbn=isbn).first()
        if exists != None:
            print isbn
        else:
            info = get_amazon_info(isbn)
            img = get_amazon_image(isbn)
            add_book(int(isbn), course['id'], info, img)
            print 'added: ' + isbn
            time.sleep(2)
