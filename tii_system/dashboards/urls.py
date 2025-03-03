from django.urls import path
from dashboards.views import *

app_name = 'dashboards'

urlpatterns = [
    # User Access
    path('', dashboard, name = 'dashboard'),
    path('transactions/', transaction, name = 'transaction'),
    path('continue-submission/<registration_code>', continue_submission, name = 'continue-submission'),
    path('detail/<registration_code>', detail, name = 'detail'),
    path('revise-submission/<registration_code>', revise_submission, name = 'revise-submission'),
    path('cancel-submission/<registration_code>', cancel_submission, name = 'cancel-submission'),
    path('tracking/', utracking, name = 'tracking'),
]
