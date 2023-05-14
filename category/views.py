from django.shortcuts import render, get_object_or_404
from bookstore.models import Book
from .models import Category
from django.utils.text import slugify
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def category(request, cat_slug=None):
    category = None
    cat_name = "All Categories"

    if cat_slug:
        #cat_slug = slugify(cat_slug)
        category = get_object_or_404(Category, slug=cat_slug)
        cat_name = category.category_name
        books = Book.objects.filter(category=category).order_by('-modified_on')
    else:
        books = Book.objects.all().order_by('-modified_on')

    paginator = Paginator(books, 20)
    page = request.GET.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'books': books,
        'category_name': cat_name,
        'category': category,  # Pass the category object to the template
    }
    return render(request, 'books-cat.html', context)
