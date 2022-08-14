import imp
from multiprocessing import context
from telnetlib import STATUS
from unicodedata import name
from django import shortcuts

from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.views import generic
from django.views.generic import ListView
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import re_path, reverse
from datetime import datetime
from datetime import timedelta
from catalog.forms import RenewBookForm,NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from catalog.models import Book

# Create your views here.
from .models import Author, Book, BookCopy


def index(request):
    num_books = Book.objects.count()
    num_copy_books = BookCopy.objects.count()
    num_copy_books_available = BookCopy.objects.filter(status=1).count()
    nums_visits=request.session.get('num_visit',0)
    request.session['num_visit']=nums_visits+1
    context = {
        'num_books':num_books,
        'num_copies':num_copy_books,
        'num_copies_available':num_copy_books_available,
        'num_visit':nums_visits,
    }
    return render(request, 'index.html',context=context)

class BookListView(ListView):
    paginate_by = 2
    model = Book

    def get_context_data(self, **kwargs):
        context=super(BookListView,self).get_context_data(**kwargs)
        context['name']='Library'
        return context

class AuthorListView(ListView):
    paginate_by = 2
    model = Author

# def BookList(request):
#     books = Book.objects.all()
#     paginator = Paginator(books, 1) # Show 25 contacts per page.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context ={
#         'book_list': books,
#         'page_obj': page_obj,
#     }
#     return render(request, 'catalog/book_list.html',context=context)

class BookDetailView(generic.DetailView):
    model = Book
class AuthorDetailView(generic.DetailView):
    model = Author

def loaned_books(request):
    num_books_loaned = BookCopy.objects.filter(status=0)
    context = {
        'num_copies_loaned':num_books_loaned,
    }
    return render(request, 'catalog/loanedbook.html',context=context)

def renew_book(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookCopy, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from t he request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_date = form.cleaned_data['renewal_date']
            # book_instance.borrower='borrower'
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('books'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.today().date() + timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew.html', context)

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect('index')
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})
# def return_book(request,pk):
#     """View function for renewing a specific BookInstance by librarian."""
#     book_instance = get_object_or_404(BookCopy, book_id=pk)

#     # If this is a POST request then process the Form data
#     if request.method == 'POST':

#         # Create a form instance and populate it with data from t he request (binding):
#         form = ReturnBookForm(request.POST)

#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             book_instance.status=False
#             # book_instance.borrower='borrower'
#             book_instance.save()

#             # redirect to a new URL:
#             return HttpResponseRedirect(reverse('books'))

#     # If this is a GET (or any other method) create the default form
#     else:
#         book_id=1
#         proposed_status = True
#         form = RenewBookForm(initial={'book_id':book_id,'status': proposed_status})

#     context = {
#         'form': form,
#         'book_instance': book_instance,
#     }

#     return render(request, 'catalog/book_return.html', context)
