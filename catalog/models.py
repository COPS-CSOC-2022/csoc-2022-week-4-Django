from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
# Create your models here.

class Book(models.Model):
    title= models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    genre= models.CharField(max_length=100)
    desc= models.TextField(null=True)
    max_price=models.PositiveBigIntegerField()
    rating=models.FloatField(default=0.0)
    link=models.CharField(max_length=200)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return f'{self.title} by {self.author}'
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
class Author(models.Model):
    name=models.CharField(max_length=100)
    desc= models.TextField(null=True)
    link=models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date=models.DateField(null=True, blank=True)
    due_date=models.DateField(null=True,blank=True)
    status=models.BooleanField(default=False)
    borrower=models.ForeignKey(User, related_name='borrower',null=True,blank=True,on_delete=models.SET_NULL)

    @property
    def is_overdue(self):
        if self.due_date and datetime.today().date()>self.due_date:
            return True
        return False

    def __str__(self):
        if self.borrow_date:
            return f'{self.book.title}, {str(self.borrow_date)}'
        else:
            return f'{self.book.title} - Available' 
    def get_author_url(self):
        return reverse('author-detail', args=[str(Author.id)])
    def get_absolute_url(self):
        return reverse('renew-book', args=[str(self.id)])
    # def get_return_url(self):
    #     return reverse('return-book', args=[str(self.id)])

class BookRating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rater=models.ForeignKey(User, related_name='rater',null=True,blank=True,on_delete=models.SET_NULL)
    rated=models.BooleanField(default=False)
    rating=models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.book.title} by {self.rater}: {self.rating}'
