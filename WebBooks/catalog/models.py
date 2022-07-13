from django.db import models
from django.urls import reverse


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Введите жанр книги", verbose_name="Жанр книги")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=20, help_text="Введите язык книги", verbose_name="Язык книги")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text="Введите имя автора", verbose_name="Имя автора")
    last_name = models.CharField(max_length=100, help_text="Введите фамилию автора", verbose_name="Фамилия автора")
    date_of_birth = models.DateField(help_text="Введите дату рождения", verbose_name="Дата рождения", null=True,
                                     blank=True)
    date_of_death = models.DateField(help_text="Введите дату смерти", verbose_name="Дата смерти", null=True, blank=True)

    # return ', '.join([author.last_name for author in self.author.all()])
    def display_book(self):
        return ', '.join([book.title for book in self.books.all()])

    display_book.short_description = 'Книги'

    def get_absolute_url(self):
        # author = Author.objects.get(pk=pk)
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return self.last_name


class Book(models.Model):
    title = models.CharField(max_length=200,
                             help_text="Введите название книги",
                             verbose_name="Название книги")
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
                              help_text="Выберите жанр книги",
                              verbose_name="Жанр книги", null=True)
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 help_text="Выберите язык книги",
                                 verbose_name="Язык книги", null=True)
    summary = models.TextField(max_length=1000,
                               help_text="Введите краткое описание книги",
                               verbose_name="Аннотация книги")
    isbn = models.CharField(max_length=13,
                            help_text="Должно содержать 13 символов",
                            verbose_name="ISBN книги")
    author = models.ManyToManyField('Author', help_text="Выберите автор книги",
                                    verbose_name="Автор книги", related_name='books')

    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])

    display_author.short_description = 'Авторы'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class Status(models.Model):
    name = models.CharField(max_length=20,
                            help_text="Введите статус экземпляра книги",
                            verbose_name="Сатус экземпляра книги")

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    inv_nom = models.CharField(max_length=20, null=True,
                               help_text="Введите инвентарный номер экземпляра",
                               verbose_name="Инвентарный номер")

    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)

    status = models.ForeignKey('Status', on_delete=models.CASCADE,
                               help_text="Изменить состояние экземпляра",
                               verbose_name="Статус экземпляра книги", null=True)
    imprint = models.CharField(max_length=200,
                               help_text="Введите издательство и год выпуска",
                               verbose_name="Издательство")
    due_back = models.DateField(null=True, blank=True,
                                help_text="Введите конец срока статуса",
                                verbose_name="Дата окончания статуса")

    def __str__(self):
        return '%s %s %s' % (self.inv_nom, self.book, self.status)
