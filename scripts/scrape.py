import urllib2
import json
from bs4 import BeautifulSoup
import re
import pickle

def process(dept_id):
    response = urllib2.urlopen('http://brown.verbacompare.com/compare/courses/?id=' + dept_id + '&term_id=5634')
    courses = json.load(response)
    return map(get_sect_ids, courses)
    
def get_sect_ids(course):
    sect_ids = map(lambda x: x['id'], course['sections'])
    return {'id': course['id'], 
            'sect_ids': sect_ids}

def get_isbns(course):
    """ 
    Given a course, return a list of unique ISBN associated with the course
    """
    return {'id':course['id'], 
            'isbns': get_isbns_sections(course['sect_ids'])}
    
def get_isbns_sections(sections):
    """
    Given a list of section ids, return a list of unique ISBNS associated with those sections
    """
    init = []
    for section in sections:
        response = urllib2.urlopen('http://brown.verbacompare.com/comparison?id=' + str(section))
        soup = BeautifulSoup(response)
        blob = str(soup.find_all('script'))
        isbns = re.findall(r'"isbn":"([^"]+)"', blob)
        init.extend(isbns)
        
    return list(set(init))
        
"""

# get list of the ids for every dept
response = urllib2.urlopen('http://brown.verbacompare.com/compare/departments/?term=5634')
data = json.load(response)
dept_ids = [x['id'] for x in data]

# list_of_courses is a list of tuples {'sect_ids': list of section ids, 'id': couse id}
processed = map(process, dept_ids)
#list_of_courses = []
#for dept in processed:
#    list_of_courses.extend(dept)

list_of_courses = [item for sublist in processed for item in sublist]

pickle.dump(list_of_courses, open('courses.p', 'wb'))

list_of_courses = pickle.load(open('courses.p','rb'))

# for every course, get the isbns of all books used in said course
list_of_books = map(get_isbns, list_of_courses)

pickle.dump(list_of_books, open('isbn.p','wb'))
"""
isbns = pickle.load(open('isbn.p','rb'))

# a list of tuples of only courses that have books
# courses_with_books = []
# for course in isbns:
#     if course['isbns'] != []:
#         courses_with_books.append(course)

courses_with_books = filter(lambda x: x["isbns"] != [], isbns)

# num_books = 0
# for course in courses_with_books:
#     num_books += len(course['isbns'])

num_books = sum(map(lambda x: len(x["isbns"]), courses_with_books))

print len(isbns)
print len(courses_with_books)
print num_books
