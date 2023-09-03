from django.db import models


# class Student(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)

class User(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=6)
    nationality = models.TextField()


class Post(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')


class Comment(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')


class Like(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')


# u=User.objects.filter(name__istartswith = 'a', name__endswith='x').values()
# u
#4) post = Post.objects.order_by('-title').filter(user__name__istartswith = 'a',user__name__endswith='x')
# p = [{ p1.user.name:p1.title} for p1 in post] --> [{'Alex': "Alex's second post"}, {'Alex': "Alex's first post"}]

# Comment.objects.all().filter(pk=1).delete()
# like = Like.objects.values('post__title').annotate(ammount=Count('post_id')).filter(ammount__gt=1)


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'stores'

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} '

class Book(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    authors = models.ManyToManyField(Author)

    class Meta:

        default_related_name = 'books'

    def __str__(self):
        return (f' {self.name} , '
                f'{self.price}$')


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)
# my_app_book_authors ( due relation in class "Book" many to many)