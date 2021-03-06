from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

from django.core.urlresolvers import reverse

import uuid # Required for unique book instances
from datetime import date

from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    #Model representing a book genre (e.g. Science Fiction, Non Fiction).

    name = models.CharField(max_length=200, help_text="Enter a book genre\
         (e.g. Science Fiction, Militar history etc.)")

    def __str__(self):
        # String for representing the Model object (in Admin site etc.)

        return self.name


class Language(models.Model):
    """
    Model representing a Language (e.g. English, French, Japanese, etc.)
    """
    name = models.CharField(max_length=200, help_text="Enter a the book's\
         natural language (e.g. English, Spanish, Japanese etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because a book can only have one author, but authors can have multiple books
    # In practice a book might have multiple authors, but not in this implementation!
    # Author as a string rather than object because it hasn't been declared yet in the file.
    # null=True, which allows the database to store a Null value if no author is selected,
    # and on_delete=models.SET_NULL, which will set the value of the author to
    # Null if the associated author record is deleted.


    summary = models.TextField(max_length=1000, help_text="Enter a brief\
         description of the book")
    isbn = models.CharField('ISBN', max_length=13, help_text="13 Character\
         <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>")

    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because genre can contain many books. Books can
    # cover many genres. Genre class has already been defined so we can specify
    # the object above.

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.id)])


    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ',   '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description  = 'Genre'


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed
    from the library).
    """

    # This type of field allocates a globally unique value for each instance
    # (one for every book you can find in the library).
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
         help_text="Unique ID for this particular book across whole library")

    # A book can have multiple bookinstances
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)

    # Date at which the book is expected to come
    # available after being borrowed or in maintenance).
    due_back = models.DateField(null=True, blank=True)

     # Deudor
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    @property
    def is_overdue(self):
        # Tell if a particular book instance is overdue (Atrasado)

        if self.due_back and date.today() > self.due_back:
            return True
        return False


    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True,
        default='m', help_text="Book availability")

    class Meta:
        ordering = ["due_back"]

        # Define a permission to allow a user to mark that a book has been returned
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        String for representing the Model object
        """

        #return '%s (%s)' % (self.id, self.book.title)
        return '{0} ({1})'.format(self.id, self.book.title)
        #return '{0}'.format(self.id)



class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        String for representing the Model object.
        """
        #return '%s, %s' % (self.last_name, self.first_name)
        return '{0}, {1}'.format(self.last_name, self.first_name)