from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("cale_statica", views.afis_statica, name="cale_statica"),
    path("cale_dinamica/<int:nr>/<str:sir>/<path:subcale>/", views.afis_dinamica, name="dinamica")
]
