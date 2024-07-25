from django.urls import path
from games import views


urlpatterns = [
    path('', views.GetAllGames.as_view()),
    path('load-game/<int:game>', views.LoadGameById.as_view()),
    path('<int:pk>', views.GetGameById.as_view()),
    path('<slug:slug>', views.GetGameBySlug.as_view()),
    path('platforms/', views.GetAllPlatforms.as_view()),
    path('genres/', views.GetAllGenres.as_view()),
    path('themes/', views.GetAllThemes.as_view()),
    path('game-modes/', views.GetAllGameModes.as_view()),
    path('player-perspectives/', views.GetAllPlayerPerspectives.as_view()),

]

