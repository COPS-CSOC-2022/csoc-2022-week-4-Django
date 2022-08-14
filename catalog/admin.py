from django.contrib import admin
from catalog.models import *

# Register your models here.

# admin.site.register(Book)
# admin.site.register(BookCopy)
# admin.site.register(BookRating)

class BookAdmin(admin.ModelAdmin):
    list_display= ('title','author','genre','rating','max_price')
    list_display_links=('title',)
    search_fields=('title','author','genre','rating')
    list_filter= ('genre','rating')
    list_editable=('genre','rating','max_price')

admin.site.register(Book,BookAdmin)
class BookCopyAdmin(admin.ModelAdmin):
    list_display= ('book','borrow_date','status','borrower')
    list_display_links=('book',)
    search_fields=('book','borrower')
    list_filter= ('book','borrow_date')
    list_editable=('status',)

admin.site.register(BookCopy,BookCopyAdmin)
class BookRatingAdmin(admin.ModelAdmin):
    list_display= ('book','rater','rated','rating')
    list_display_links=('book',)
    search_fields=('book','rating')
    list_filter= ('book','rating')
    list_editable=('rating',)

admin.site.register(BookRating,BookRatingAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display= ('name',)

admin.site.register(Author,AuthorAdmin)
