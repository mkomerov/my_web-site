# Импорт необходимых модулей Django
from django.db import models  # Модуль для создания моделей базы данных
from django.utils.text import slugify  # Функция для создания URL-дружественных строк

# Модель категории товаров
class Category(models.Model):
    name = models.CharField(max_length=100)  # Поле для названия категории (максимум 100 символов)
    slug = models.CharField(max_length=100, unique=True)  # Уникальное поле для URL (максимум 100 символов)

    # Переопределение метода сохранения объекта
    def save(self, *args, **kwargs):
        if not self.slug:  # Проверка, заполнено ли поле slug
            self.slug = slugify(self.name)  # Автоматическое создание slug из названия
        super().save(*args, **kwargs)  # Вызов оригинального метода сохранения

    # Метод для строкового представления объекта
    def __str__(self):
        return self.name  # Возвращает название категории при отображении объекта
    

# Модель размеров товаров
class Size(models.Model):
    name = models.CharField(max_length=20)  # Поле для названия размера (максимум 20 символов)

    # Метод для строкового представления объекта
    def __str__(self):
        return self.name  # Возвращает название размера при отображении объекта
    

# Промежуточная модель для связи товаров с размерами и отслеживания остатков
class ProductSize(models.Model):
    # Связь с моделью Product (многие к одному)
    product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                related_name='product_sizes')  # CASCADE - удаление при удалении товара
    # Связь с моделью Size (многие к одному)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)  # CASCADE - удаление при удалении размера
    stock = models.PositiveIntegerField(default=0)  # Поле для количества товара (только положительные числа)

    # Метод для строкового представления объекта
    def __str__(self):
        return f"{self.size.name} ({self.stock} in stock) for {self.product.name}"  # Форматированная строка с информацией


# Основная модель товара
class Product(models.Model):
    name = models.CharField(max_length=100)  # Название товара (максимум 100 символов)
    slug = models.CharField(max_length=100, unique=True)  # Уникальный URL-идентификатор товара
    # Связь с категорией (многие к одному)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='products')  # CASCADE - удаление при удалении категории
    color = models.CharField(max_length=100)  # Цвет товара (максимум 100 символов)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена (10 цифр всего, 2 после запятой)
    description = models.TextField(blank=True)  # Описание товара (может быть пустым)
    main_image = models.ImageField(upload_to='products/main/')  # Главное изображение (путь для загрузки)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания (автоматически при создании)
    updated_at = models.DateTimeField(auto_now=True)  # Дата обновления (автоматически при сохранении)

    # Переопределение метода сохранения объекта
    def save(self, *args, **kwargs):
        if not self.slug:  # Проверка, заполнено ли поле slug
            self.slug = slugify(self.name)  # Автоматическое создание slug из названия
        super().save(*args, **kwargs)  # Вызов оригинального метода сохранения
    
    # Метод для строкового представления объекта
    def __str__(self):
        return self.name  # Возвращает название товара при отображении объекта
    

# Модель для дополнительных изображений товара
class ProductImage(models.Model):
    # Связь с товаром (многие к одному)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                related_name='images')  # CASCADE - удаление при удалении товара
    image = models.ImageField(upload_to='products/extra/')  # Дополнительное изображение (путь для загрузки)