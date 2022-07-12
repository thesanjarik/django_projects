from django.db import models

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
    name = models.CharField(max_length=100, verbose_name='Названия')

    def __str__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    name = models.CharField(max_length=100, verbose_name='Названия')

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 null=True, verbose_name='Категории')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Тэги')
    name = models.CharField(max_length=1000, unique=True, verbose_name='Названия')
    description = models.TextField(blank=True, verbose_name='Названия')
    price = models.FloatField(verbose_name='Цена (в долларах)')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменение')
    image = models.ImageField(upload_to='products', null=True, verbose_name='Картинка')


    def __str__(self):
        return self.name

    @property
    def tag_list(self):
        return ', '.join([tag.name for tag in self.tags.all()])


class Review(models.Model):
    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
    text = models.TextField(verbose_name='Текст отзывы')
    author = models.CharField(verbose_name='Автор', max_length=100, null=True, blank=True, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews',
                                verbose_name='Товар')

    def __str__(self):
        return self.text

from django.contrib.auth.models import User


class ConfirmCode(models.Model):
    code = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
