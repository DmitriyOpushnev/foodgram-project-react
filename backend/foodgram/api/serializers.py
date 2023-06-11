from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from recipes.models import (AmountIngredients, Favourite, Ingredient, Recipe,
                            ShopingCart, Tag)
from users.models import Subscription, User


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'password',
        )
        read_only_fields = ('is_subscribed', )
        extra_kwargs = {'password': {'write_only': True}, }

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and user != obj and user.follower.filter(
            author=obj).exists()

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SubscribeListSerializer(CustomUserSerializer):
    """Сериализатор для получения подписок."""
    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes_count', 'recipes',
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name', )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[: int(limit)]
        serializer = RecipeShortSerializer(recipes, many=True, read_only=True)
        return serializer.data


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания подписки."""
    class Meta:
        model = Subscription
        fields = ('author', 'user',)

    def validate(self, data):
        author_id = self.context.get(
            'request').parser_context.get('kwargs').get('id')
        author = get_object_or_404(User, id=author_id)
        user = self.context.get('request').user
        if user.follower.filter(author=author_id).exists():
            raise ValidationError(
                detail='Вы уже подписаны на пользователя.',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise ValidationError(
                detail='Подписка на себя невозможна.',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data

    def create(self, validated_data):
        return Subscription.objects.create(**validated_data)

    def to_representation(self, instance):
        return SubscribeListSerializer(
            instance=instance.author, context=self.context
        ).data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор полей избранных рецептов и покупок."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра ингридиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class ReadIngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор связи ингридиентов и рецепта при чтении рецепта."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AmountIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра рецепта."""
    tags = TagSerializer(read_only=False, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = ReadIngredientRecipeSerializer(many=True, source='portions')
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(max_length=None)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time',
        )

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        return user.is_authenticated and user.favorites.filter(
            recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        return user.is_authenticated and user.shopping_list.filter(
            recipe=recipe).exists()


class WriteIngredientPortionSerializer(serializers.ModelSerializer):
    """Сериализатор связи ингридиентов и рецепта при записи рецепта."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = AmountIngredients
        fields = ('id', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецепта."""
    ingredients = WriteIngredientPortionSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        error_messages={'does_not_exist': 'Указанного тега не существует.'}
    )
    image = Base64ImageField(max_length=None)

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time'
        )

    def validate_tags(self, tags):
        if len(set(tags)) != len(tags):
            raise serializers.ValidationError(
                'Передаваемые тэги не уникальны')
        for tag in tags:
            if not Tag.objects.filter(id=tag.id).exists():
                raise serializers.ValidationError(
                    'Указанного тега не существует')
        return tags

    def validate_cooking_time(self, cooking_time):
        if not 1 <= cooking_time <= 600:
            raise serializers.ValidationError(
                'Время приготовления должно от 1 минуты до 10 часов')
        return cooking_time

    def validate_ingredients(self, ingredients):
        unique_items = set(
            tuple(ingredient.items()) for ingredient in ingredients
        )
        if len(unique_items) != len(ingredients):
            raise serializers.ValidationError(
                'Передаваемые ингредиенты не уникальны')
        if not ingredients:
            raise serializers.ValidationError(
                'Отсутствуют ингридиенты')
        for ingredient in ingredients:
            if 0 >= int(ingredient.get('amount')) > 5000:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть больше 0 и меньше 5000'
                )
        return ingredients

    @staticmethod
    def add_ingredients_and_tags(self, ingredients, tags, recipe):
        recipe.tags.set(tags)
        AmountIngredients.objects.bulk_create([AmountIngredients(
            recipe=recipe,
            ingredient=ingredient['id'],
            amount=ingredient['amount'],
        ) for ingredient in ingredients])
        return recipe

    def create(self, validated_data):
        user = self.context['request'].user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=user, **validated_data)
        self.add_ingredients_and_tags(ingredients, tags, recipe)
        return recipe

    def update(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe.tags.clear()
        recipe.ingredients.clear()
        AmountIngredients.objects.filter(recipe=recipe).delete()
        self.add_ingredients_and_tags(ingredients, tags, recipe)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class FavouriteSerializer(serializers.ModelSerializer):
    """ Сериализатор избранных рецептов."""

    class Meta:
        model = Favourite
        fields = ('user', 'recipe', )

    def validate(self, data):
        user = data['user']
        if user.favorites.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное.'
            )
        return data

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""

    class Meta:
        model = ShopingCart
        fields = ('user', 'recipe', )

    def validate(self, data):
        user = data['user']
        if user.shopping_list.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в корзину'
            )
        return data

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
