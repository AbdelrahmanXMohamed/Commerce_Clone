from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.WatchListPage, name="mywatchlist"),
    path("mywatchlist/<int:id>",views.WatchList_remove,name="watchlistremove"),
    path("watchlist/<int:id>", views.functions_WatchList, name="watchlist"),
    path("details/<int:product>", views.details, name="details"),
    path("category",views.CategoryPage,name="category"),
    path("category/<int:id>",views.Categoryitems,name="categoryitem"),
    path("add_comment/<int:id>",views.add_comment,name="add_comment"),
    path("add_bids/<int:id>",views.bid, name="add_bids")
]
