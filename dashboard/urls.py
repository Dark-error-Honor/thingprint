from django.urls import path

from .views import *

urlpatterns = [
    path('', main_dashboard_view),
    path('create/', create_thing_view),
    path('manage/', manage_things_view),
    path('edit/<int:id>', edit_thing_view),
    path('remove/<int:id>', remove_thing_view),
]
