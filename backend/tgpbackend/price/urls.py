from django.urls import path
from price import views

# Create your views here.
urlpatterns = [
    path('load/', views.LoadPriceByGameId.as_view()),
    path('get-game-price/<slug:game_slug>/<str:currency>/', views.GetAllGamePrices.as_view()),
]
