from django.urls import path
from .views import Petview, PetDetailView

urlpatterns = [
    path("pets/", Petview.as_view()),
    path("pets/<int:pet_id>/", PetDetailView.as_view()),
]
