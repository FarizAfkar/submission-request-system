from django.urls import path
from . import views

app_name = 'c-panels'

urlpatterns = [
    path('', views.cpanel_list, name = 'list-transaction'),
    path('approval/<registration_code>', views.cpanel_approval, name = 'approval-transaction'),
    path('reject/<registration_code>', views.cpanel_reject, name = 'reject-transaction'),
]
