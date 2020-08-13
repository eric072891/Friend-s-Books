from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.db.models import Count

from .models import Book, Goodreads_Id
from .forms import IdForm
from django.shortcuts import redirect, render

import json
import requests
import xmltodict
from math import floor

key = 'PmNpwtnxrtM6TiYdck3S3Q'

# check if a valid id
# check if in database
# if first but not second, do api requests to put books into database and move on to categorization
# if in database, just return already existing results.
def ids_and_input_data(request):
    if request.method == 'POST':

        form = IdForm(request.POST)

        if form.is_valid():

            #get userid from the form
            userId = form.cleaned_data['id']
            print(userId)

            # check if user input is a valid goodreads id
            valid = requests.get(f'https://www.goodreads.com/review/list/{userId}.xml?key={key}&v=2&shelf=to-read')



            # check if user input is a valid goodreads id
            if valid.status_code == 404:
                return redirect('invalid_id')

            # check if id is in database, if so, go directly to book categories of user
            # need to check what happens when no such user id is in database
            else:


                #if Goodreads_Id.objects.filter(id=userId).exists():
                    # I want to redirect to the categories page using the current user id
                    #return redirect('categories', id=userId)

                if True:
                    #save new user id
                    g = Goodreads_Id(id=userId)
                    g.save()

                    #find the number of total requests I have to make, given that I have a limit of 200 books per request
                    total_dict = xmltodict.parse(valid.content)
                    total = total_dict["GoodreadsResponse"]["reviews"]["@total"]
                    num_requests = floor(int(total) / 200) + 1

                    if num_requests > 1:
                        for i in range(num_requests-1):
                            #make a goodreads request
                            pageNum = str(i+1)
                            Goodreads_request = requests.get(f'https://www.goodreads.com/review/list/{userId}.xml?key={key}&v=2&shelf=to-read&page={pageNum}')
                            Goodreads_dict = xmltodict.parse(Goodreads_request.content)

                            for j in range(200):
                                # store goodreads isbn 13 and title for the book
                                isbn13 = Goodreads_dict['GoodreadsResponse']['reviews']['review'][j]['book']['isbn13']
                                title = Goodreads_dict['GoodreadsResponse']['reviews']['review'][j]['book']['title']
                                search_title = title.replace(' ', '+')

                                # search google books api for the corresponding request
                                g = requests.get(
                                    'https://www.googleapis.com/books/v1/volumes?q=intitle:' + title + '+isbn:' + isbn13)
                                google_dict = json.loads(g.content)

                                # store the category, maturity rating, and page count found from the google books api
                                category = google_dict["items"][0]['volumeInfo']['categories'][0]
                                maturityRating = google_dict["items"][0]['volumeInfo']['maturityRating']
                                pageCount = google_dict["items"][0]['volumeInfo']['pageCount']

                                book_row = Book(userid=userId, title=title, isbn13=isbn13, pagecount=pageCount,
                                                maturityrating=maturityRating, category=category)
                                book_row.save()



                    #remainder is what's left over after processing the batches of 200 books
                    remainder = int(total)-200*(num_requests-1)

                    # make good reads request, page is the total number of requests
                    pageNum = num_requests
                    Goodreads_request = requests.get(f'https://www.goodreads.com/review/list/{userId}.xml?key={key}&v=2&shelf=to-read&page={pageNum}')
                    Goodreads_dict = xmltodict.parse(Goodreads_request.content)
                    for i in range(remainder):
                        # store information per book along with relevant information from the google api
                        # store goodreads isbn 13 and title for the book
                        isbn13 = Goodreads_dict['GoodreadsResponse']['reviews']['review'][i]['book']['isbn13']
                        title = Goodreads_dict['GoodreadsResponse']['reviews']['review'][i]['book']['title']
                        search_title = title.replace(' ', '+')

                        # search google books api for the corresponding request
                        g = requests.get(
                            'https://www.googleapis.com/books/v1/volumes?q=intitle:' + title + '+isbn:' + isbn13)
                        google_dict = json.loads(g.content)

                        # store the category, maturity rating, and page count found from the google books api
                        category = google_dict["items"][0]['volumeInfo']['categories'][0]
                        maturityRating = google_dict["items"][0]['volumeInfo']['maturityRating']
                        pageCount = google_dict["items"][0]['volumeInfo']['pageCount']

                        book_row = Book(title=title, isbn13=isbn13, pagecount=pageCount, maturityrating=maturityRating, category=category)
                        book_row.userid_id = userId
                        book_row.save()

                    return redirect('categories', id=userId)
    else:
        form = IdForm()
    return render(request, 'bookviewer/id_input.html', {'form': form})


def invalid_id(request):
    template = loader.get_template('bookviewer/invalid_id.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def categories(request, id):
    book_categories = Book.objects.values('category').order_by('category').annotate(count=Count('category'))
    template = loader.get_template('bookviewer/categories.html')

    context = {
        'categories': book_categories,
        'id': id,
    }
    return HttpResponse(template.render(context, request))


def book_category(request, cat, id):
    books_in_category = Book.objects.filter(category=cat, userid=id).order_by('title')
    template = loader.get_template("bookviewer/book_category.html")
    context = {
        'category': cat,
        'books': books_in_category
    }

    return HttpResponse(template.render(context, request))


def detail(request, title):
    return HttpResponse("You're looking at {}.".format(title))
