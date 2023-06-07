from django.contrib import admin
from django.utils.html import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from core.texts import EMPTY_STRING
from recipes.models import (AmountIngredients, Favourite, Ingredient, Recipe,
                            ShopingCart, Tag)


class IngredientUpload(resources.ModelResource):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagUpload(resources.ModelResource):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientUpload]
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name', )
    search_fields = ('name',)
    empty_value_display = EMPTY_STRING


class AmountIngredientsInline(admin.TabularInline):
    model = AmountIngredients


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    fields = (
        'name', 'cooking_time',
        'author', 'tags',
        'text', 'image',
        'short_image'
    )
    inlines = [
        AmountIngredientsInline,
    ]
    search_fields = ('author', 'name', 'tags',)
    readonly_fields = ('short_image',)
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = EMPTY_STRING

    @admin.display(description='Иконка')
    def short_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" height="60">')


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    resource_classes = [TagUpload]
    list_display = ('name', 'slug', 'color',)
    empty_value_display = EMPTY_STRING


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)


@admin.register(ShopingCart)
class ShopingCart(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
