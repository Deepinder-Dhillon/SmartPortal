from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import login, logout, get_patients, create_patient, delete_patient, set_current_patient, get_current_patient, unset_current_patient, search_patients, update_patient

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("patients/", get_patients, name="get_patients"),
    path("patients/create/", create_patient, name="create_patient"),
    path("patients/<int:phn>/delete/", delete_patient, name="delete_patient"),
    path("patients/<int:phn>/set-current/", set_current_patient, name="set_current_patient"),
    path("patients/current/", get_current_patient, name="get_current_patient"),
    path("patients/unset-current/", unset_current_patient, name="unset_current_patient"),
    path("patients/search/", search_patients, name="search_patients"),
    path("patients/<int:original_phn>/update/", update_patient, name="update_patient"),
]
