from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (CASCADE, CharField, DateTimeField, ForeignKey,
                              ImageField, ManyToManyField, Model,
                              PositiveSmallIntegerField, SlugField, TextField,
                              UniqueConstraint)

from api.validators import validate_clean_text
from core.limits import Limits
from core.texts import (HELP_TEXT_FOR_COOKING_TIME, HELP_TEXT_FOR_HEX_COLOR,
                        HELP_TEXT_FOR_INGREDIENT_TAG_RECIPE,
                        HELP_TEXT_FOR_INGRIDIENTS_AMOUNT)
from users.models import User


class Ingredient(Model):
    """Модель ингредиента для приложения Foodgram."""

    REQUIRED_FIELDS = ('name', 'measurement_unit',)

    name = CharField(
        verbose_name='Название',
        max_length=Limits.INGRIDIENT_RECIPE_FIELDS_TAG_LENGHT.value,
        db_index=True,
        help_text=HELP_TEXT_FOR_INGREDIENT_TAG_RECIPE,
    )
    measurement_unit = CharField(
        verbose_name='Единица измерения',
        max_length=Limits.INGRIDIENT_RECIPE_FIELDS_TAG_LENGHT.value,
        help_text=HELP_TEXT_FOR_INGREDIENT_TAG_RECIPE,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement_unit'
            )
        ]
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(Model):
    """Модель тега для приложения Foodgram."""

    REQUIRED_FIELDS = ('name', 'color', 'slug',)

    name = CharField(
        verbose_name='Название',
        max_length=Limits.INGRIDIENT_RECIPE_FIELDS_TAG_LENGHT.value,
        unique=True,
        help_text=HELP_TEXT_FOR_INGREDIENT_TAG_RECIPE,
        validators=[validate_clean_text],
    )
    color = ColorField(
        format='hex',
        verbose_name='HEX-код',
        max_length=Limits.HEX_COLOR_FIELD_LENGHT.value,
        unique=True,
        help_text=HELP_TEXT_FOR_HEX_COLOR,
    )
    slug = SlugField(
        verbose_name='Метка',
        max_length=Limits.INGRIDIENT_RECIPE_FIELDS_TAG_LENGHT.value,
        unique=True,
        help_text=HELP_TEXT_FOR_INGREDIENT_TAG_RECIPE,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} {self.color}'


class Recipe(Model):
    """Модель рецепта для приложения Foodgram."""

    REQUIRED_FIELDS = (
        'author', 'name', 'text', 'image',
        'ingredients', 'tags', 'cooking_time',
    )

    author = ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipes',
        on_delete=CASCADE,
    )
    name = CharField(
        verbose_name='Название',
        max_length=Limits.INGRIDIENT_RECIPE_FIELDS_TAG_LENGHT.value,
        help_text=HELP_TEXT_FOR_INGREDIENT_TAG_RECIPE,
    )
    text = TextField(
        verbose_name='Описание',
        help_text='Обязательное для заполнения поле.',
        validators=[validate_clean_text],
    )
    image = ImageField(
        verbose_name='Картинка',
        upload_to='images/',
        help_text='Обязательное для заполнения поле.',
    )
    ingredients = ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        related_name='recipes',
        through='AmountIngredients',
    )
    tags = ManyToManyField(
        Tag,
        verbose_name='Список тегов',
        related_name='recipes',
    )
    cooking_time = PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        default=Limits.MIN_COOKING_TIME.value,
        validators=[MinValueValidator(
            Limits.MIN_COOKING_TIME.value,
            message='Время приготовления не может быть меньше одной минуты'
        ), MaxValueValidator(
            Limits.MAX_COOKING_TIME.value,
            message='Время приготовления не может быть больше десяти часов')],
        help_text=HELP_TEXT_FOR_COOKING_TIME,
    )
    pub_date = DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.name}. Автор: {self.author.username}'


class AmountIngredients(Model):
    """Модель количества ингредиентов для приложения Foodgram."""

    REQUIRED_FIELDS = ('recipe', 'ingredient', 'amount',)

    recipe = ForeignKey(
        Recipe,
        verbose_name='Связанные рецепты',
        related_name='ingredient',
        on_delete=CASCADE,
    )
    ingredient = ForeignKey(
        Ingredient,
        verbose_name='Наименование ингредиентов',
        related_name='recipe',
        on_delete=CASCADE,
    )
    amount = PositiveSmallIntegerField(
        verbose_name='Количество ингредиентов',
        default=Limits.MIN_INGREDIENTS_AMOUNT.value,
        validators=[MinValueValidator(
                Limits.MIN_INGREDIENTS_AMOUNT.value,
                message='Количество ингредиентов не может быть меньше одного'
            )],
        help_text=HELP_TEXT_FOR_INGRIDIENTS_AMOUNT,
    )

    class Meta:
        verbose_name = 'Количество ингридиентов'
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ('recipe', )

    def __str__(self):
        return f'{self.amount} {self.ingredient}'


class Favourite(Model):
    """Модель избранного рецепта для приложения Foodgram."""

    recipe = ForeignKey(
        Recipe,
        verbose_name='Понравившиеся рецепты',
        related_name='favorites',
        on_delete=CASCADE,
    )
    user = ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorites',
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipe_user'
            )
        ]
        ordering = ('user',)

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в избранное'


class ShopingCart(Model):
    """Модель списка покупок для приложения Foodgram."""

    recipe = ForeignKey(
        Recipe,
        verbose_name='Рецепт в списке покупок',
        related_name='shopping_list',
        on_delete=CASCADE,
    )
    user = ForeignKey(
        User,
        verbose_name='Пользователь создавший список покупок',
        related_name='shopping_list',
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_cart_user'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в корзину'
