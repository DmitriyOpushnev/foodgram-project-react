from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CustomTokenCreateView, IngredientViewSet, RecipeViewSet,
                       TagViewSet, UserViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = (
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/token/login/', CustomTokenCreateView.as_view(), name='login'),
    path('auth/', include('djoser.urls.authtoken')),
)
