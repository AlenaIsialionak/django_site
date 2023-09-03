import dataclasses
import logging
import sys

from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from my_app.models import Book, Store, Author, Publisher
from my_app.utils import query_debugger
from django.db.models import Prefetch, Subquery

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s "
           "[%(name)s:%(funcName)s:%(lineno)s] -> %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
    stream=sys.stdout,
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)
django_logger = logging.getLogger('django.db.backends')
django_logger.setLevel(logging.DEBUG)
django_logger.addHandler(logging.StreamHandler())


@query_debugger(logger)
def _get_all_books():
    """
    Lesson 3: Using select_related for ForeignKey
    """
    # queryset = Book.objects.all()
    # logger.warning(f"SQL: {str(queryset.query)}")
    """
    Один запрос для заполнения всех книг и, выполняя итерацию каждый раз, 
    мы получаем доступ к издателю, который выполняет другой отдельный запрос.
    Давайте изменим запрос с помощью select_related следующим образом и посмотрим, что произойдет.
    """
    queryset = Book.objects.select_related("publisher")
    logger.warning(f"SQL: {str(queryset.query)}")

    return [
        {
            'id': book.id, 'name': book.name,
            # here the additional SQL query is executed to get a publisher name
            'publisher': book.publisher.name
        }
        for book in queryset
    ]


@query_debugger(logger)
def _get_all_stores():
    """
    Lesson 3: Using prefetch_related for ManyToManyField
    """
    # queryset = Store.objects.all()
    # logger.warning(f"SQL 1: {str(queryset.query)}")
    """
    У нас в базе 10 магазинов и в каждом магазине по 10 книг. 
    Здесь происходит один запрос для выборки всех хранилищ, 
    и во время итерации по каждому хранилищу выполняется другой запрос, 
    когда мы получаем доступ к полю books ManyToMany.
    Давайте уменьшим количество запросов с помощью prefetch_related
    """
    queryset = Store.objects.prefetch_related("books")
    logger.warning(f"SQL: {str(queryset.query)}")

    stores = []
    for store in queryset:
        all_books = store.books.all()
        books = [book.name for book in all_books]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return stores


@query_debugger(logger)
def _get_stores_with_expensive_books():
    # queryset = Store.objects.prefetch_related('books')
    # logger.warning(f"SQL 1: {str(queryset.query)}")
    """
    Here we need to use additional Prefetch object
    because in query as *queryset = Store.objects.prefetch_related('books')*
    ALL books related to the existing Stores will be joined and retrieved,
    but then we need to filter these Books by the price range, and this
    will override the first Join

    """
    queryset = Store.objects.prefetch_related(
        Prefetch(
            'books',
            queryset=Book.objects.filter(price__range=(250, 300))
        )
    )

    stores = []
    for store in queryset:
        stores_filtered = store.books.all()
        books = [book.name for book in stores_filtered]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return stores


@query_debugger(logger)
def _get_authors_with_expensive_books():
    queryset = Book.objects.filter(price__gte=250).prefetch_related('authors')
    logger.warning(f'SQL: {str(queryset.query)}')

    books = []
    for b in queryset:
        all_authors = b.authors.all()
        authors = [a.first_name for a in all_authors]
        books.append({'book': b.name, 'price': b.price, 'author': authors})
    return books

@query_debugger(logger)
def _get_all_publishers():
    """
    prefetch_related is used for 'Reversed ManyToOne relation' as for 'ManyToMany field'
    """
    # Publisher model doesn't have static 'books' field,
    # but Book model has static 'publisher' field as ForeignKey
    # to the Publisher model. In context of the Publisher
    # model the 'books' is dynamic attribute which provides
    # Reverse ManyToOne relation to the Books
    publishers = Publisher.objects.prefetch_related('books')

    publishers_with_books = []
    for p in publishers:
        books = [book.name for book in p.books.all()]
        publishers_with_books.append(
            {'id': p.id, 'name': p.name, 'books': books}
        )

    return publishers_with_books


@query_debugger(django_logger)
def _get_publishers_with_expensive_books():
    """
    Lesson 4: SubQuery example
    """
    expensive_books = Book.objects.filter(price__gte=200)

    # N queries:
    # publishers_ids = [book.publisher.id for book in expensive_books]
    # publishers_with_expensive_books = Publisher.objects.filter(id__in=publishers_ids)

    # Only one query:
    publishers_with_expensive_books = Publisher.objects.filter(
        id__in=Subquery(expensive_books.values('publisher'))
    )
    logger.info(f"SQL: {publishers_with_expensive_books.query}")

    return [item for item in publishers_with_expensive_books.values()]

@query_debugger(django_logger)
def _get_expensive_books():

    expensive_books = Book.objects.filter(price__gte=200).order_by('-price')
    books = [{'name': b.name, 'price': b.price} for b in expensive_books]
    return books

def _get_all_authors():
    authors = Author.objects.all().order_by('last_name')
    return [(a.first_name, a.last_name) for a in authors]


# ENDPOINTS
def get_all_books(request: HttpRequest) -> HttpResponse:
    books_list = _get_all_books()
    return HttpResponse(f"All Books from Stores:\n {books_list}")


def get_all_stores(request: HttpRequest) -> HttpResponse:
    stores_list = _get_all_stores()
    return HttpResponse(f"All Stores:\n {stores_list}")


def get_stores_with_expensive_books(request: HttpRequest) -> HttpResponse:
    stores_list = _get_stores_with_expensive_books()
    return HttpResponse(f"Stores with expensive books:\n {stores_list}")


def get_all_publishers(request: HttpRequest) -> HttpResponse:
    pubs = _get_all_publishers()
    return HttpResponse(f"All Publishers:\n {pubs}")


def get_publishers_with_expensive_books(request: HttpRequest) -> HttpResponse:
    authors = _get_publishers_with_expensive_books()
    return HttpResponse(f"Publishers with expensive books:\n {authors}")


def get_book_by_id(request: HttpRequest, book_id: int) -> HttpResponse:
    if not (book := Book.objects.filter(id=book_id).first()):
        return HttpResponseNotFound(
            f'<h2>Book by id {book_id} not found</h2>'
        )

    authors = book.authors.all()
    authors = "<h2><p>".join([str(a) for a in authors])
    logger.debug(authors)
    return HttpResponse(
        f"<h1>Found book: {book}, authors: <h2><p>{authors}</h1>"
    )


def hello(request: HttpRequest) -> HttpResponse:
    return HttpResponse(f"Hello World!")


# HOMEWORK
def get_expensive_books(request: HttpRequest) -> HttpResponse:
    expensive_books = _get_expensive_books()
    return HttpResponse(f"Expensive books : <p>{expensive_books}</p>")

def get_all_authors(request: HttpRequest) -> HttpResponse:
    authors = _get_all_authors()
    return HttpResponse(f'All authors:<p> {authors}')


def get_authors_with_expensive_books(request: HttpRequest) -> HttpResponse:
    authors = _get_authors_with_expensive_books()
    return HttpResponse(f"Authors with expensive books:\n {authors}")


def get_publisher_by_id(request: HttpRequest, publisher_id: int) -> HttpResponse:
    if not (publisher := Publisher.objects.filter(id=publisher_id).first()):
        return HttpResponseNotFound(
            f'<h2>Book by id {publisher_id} not found</h2>'
        )

    book_s = publisher.books.all()
    book_s= "<h2><p>".join([str(b) for b in book_s])
    logger.debug(book_s)
    return HttpResponse(
        f"<h1>Found publisher: {publisher},<hr> Books: <h2>{book_s}</h1>"
    )

<<<<<<< HEAD
=======

>>>>>>> e58c06c (lesson)
def get_store_by_id(request: HttpRequest, store_id: int) -> HttpResponse:
    pass


def get_author_by_id(request: HttpRequest, author_id: int) -> HttpResponse:
    pass