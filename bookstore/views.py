from contextlib import _RedirectStream
from django.shortcuts import render,get_object_or_404
from .models import Book
from category.models import Category
from checkout.models import order_list
from checkout.models import order
from checkout.models import invoice
from accounts.models  import Account
from checkout.models import invoice
from django.contrib import messages
from django.contrib.auth.decorators import  login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import requests

categories_list = Category.objects.all()


#adding paging


"""def home(request):

    books = Book.objects.all()[0:20]
    font_page_context = {
        'books': books,
    }
    return render(request, 'index.html',font_page_context)"""


def home(request):
    # Make API call to retrieve book data
    api_url = 'https://www.googleapis.com/books/v1/volumes?q=subject:fiction:&printType=books&maxResults=30&startIndex=100'

    response = requests.get(api_url)
    books_data = response.json().get('items', [])

    # Extract book data and create Book objects
    books = []
    for book_data in books_data:
        volume_info = book_data.get('volumeInfo', {})
        price_info = volume_info.get('saleInfo', {}).get('listPrice', {})
        book = Book(
            title=volume_info.get('title', ''),
            author=volume_info.get('authors', [''])[0],
            description=volume_info.get('description', ''),
            cover_image_url=volume_info.get('imageLinks', {}).get('thumbnail', ''),
            price=price_info.get('amount') if price_info else 300,
           # currency=price_info.get('currencyCode') if price_info else 300,
            category=Category.objects.get_or_create(volume_info.get('categories', [''])[0])[0],
            slug=book_data.get('title', ''),  # Set the slug to the book's ID
        


        
        )
        books.append(book)
        book.save()

    # Render template with context data
    font_page_context = {
        'books': books,
    }
    return render(request, 'index.html', font_page_context)
def contact(request):


    return render(request, 'contact-us.html')

def about(request):

    return render(request, 'about.html')

def single_book(request, single_book_slug):
    if single_book_slug is not None:
        book = get_object_or_404(Book,slug=single_book_slug)
        related_books = Book.objects.filter(category=book.category).exclude(slug=single_book_slug)[:5]


         
        context = {

            'book': book,
            'related_books': related_books,

        }

    return render(request, 'book-single-page.html',context)


def search_result(request):
    if 'query' in request.GET:
        query = request.GET['query']
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
        response = requests.get(url)
        data = response.json()
        books = []

        for item in data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            price_info = volume_info.get('saleInfo', {}).get('listPrice', {})
            book = Book(
            title=volume_info.get('title', ''),
            author=volume_info.get('authors', [''])[0],
            description=volume_info.get('description', ''),
            cover_image_url=volume_info.get('imageLinks', {}).get('thumbnail', ''),
            price=price_info.get('amount') if price_info else 300,
           # currency=price_info.get('currencyCode') if price_info else 300,
            category=Category.objects.get_or_create(volume_info.get('categories', [''])[0])[0],
            slug=item.get('title', ''),  # Set the slug to the book's ID
        
            )
            books.append(book)
            book.save()

        context = {
            'books': books,
        }
        return render(request, 'search_res.html', context)



@login_required(login_url="/login")
def orders(request):
        if request.user.is_authenticated:
            user = Account.objects.get(email=request.user.email)
            order_id = order.objects.all().filter(client=user).order_by('date_created')

            all_orders = Paginator(order.objects.all().filter(client=user).order_by('-date_created'), 10)
            page = request.GET.get('page')

            try:
                orders = all_orders.page(page)
            except PageNotAnInteger:
                orders = all_orders.page(1)
            except EmptyPage:
                orders=  all_orders.page(all_orders.num_pages)

            context={

                'order_id_list' : orders,
            }
            return render(request,"list-orders.html",context)
        else:
            messages.error("Sorry, you need to be logged in to view your orders")
            return redirect("login")

@login_required(login_url="/login")
def view_order(request, order_id):
      if request.user.is_authenticated:

          print(order_id)
          order_items_list = order_list.objects.all().filter(order_id=order_id)
          invoice_details = invoice.objects.all().filter(order_id=order_id)



          context={
              "order_id":order_id,

              "order_items_list":order_items_list,
              "invoice_list": invoice_details
          }
          return render(request,"view_order.html",context=context)
      else:
          return redirect('login')


@login_required(login_url="/login")
def view_invoice(request, invoice_id):
     if request.user.is_authenticated:
         invoice_dat = invoice.objects.get(invoice_id=invoice_id)

         context = {

             'invoice':invoice_dat

         }
         return render(request,"view_invoice.html",context=context)
     else:
         return _RedirectStream("login")




