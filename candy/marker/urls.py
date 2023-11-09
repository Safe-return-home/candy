from django.urls import path
from .views import marker_view, marker_edit_view, marker_detail_view, marker_police_view, marker_detail_delete

app_name = "marker"

urlpatterns = [
    path('', marker_view, name="markers"),
    path('<int:pk>/', marker_detail_view, name="marker_detail"),
    path('edit/', marker_edit_view, name="marker_edit"),
    path('police/', marker_police_view, name="police"),
    path('delete/<int:pk>/', marker_detail_delete, name="detail_delete"),
]
