from django.urls import path
from transactions.views import *

app_name = 'transactions'

urlpatterns = [
    # Opening-representative
    path('opening-representative/renewal-type/', renewal_type_representative, name = 'renewal_type_representative'),
    path('opening-representative/renew-list/', renew_list_representative, name = 'renew_list_representative'),
    path('opening-representative/us/', openingrepresentativeUS, name = 'openingrepresentativeUS'),
    path('opening-representative/id/', openingrepresentativeID, name = 'openingrepresentativeID'),
    path('opening-representative/applicant/', openingrepresentativeApplicant, name = 'openingrepresentativeApplicant'),

    # Appointing-agent-distributor
    path('appointing-agent-distributor/renewal-type/', renewal_type_agentdistributor , name = 'renewal_type_agentdistributor'),
    path('appointing-agent-distributor/renew-list/', renew_list_agentdistributor , name = 'renew_list_agentdistributor'),
    path('appointing-agent-distributor/us/', appointingagentdistributorUS, name = 'appointingagentdistributorUS'),
    path('appointing-agent-distributor/id/', appointingagentdistributorID, name = 'appointingagentdistributorID'),
    path('appointing-agent-distributor/applicant/', appointingagentdistributorApplicant, name = 'appointingagentdistributorApplicant'),

    # Appointing-franchise
    path('appointing-franchise/renewal-type/', renewal_type_franchise , name = 'renewal_type_franchise'),
    path('appointing-franchise/renew-list/', renew_list_franchise , name = 'renew_list_franchise'),
    path('appointing-franchise/us/', appointingfranchiseUS, name = 'appointingfranchiseUS'),
    path('appointing-franchise/id/', appointingfranchiseID, name = 'appointingfranchiseID'),
    path('appointing-franchise/applicant/', appointingfranchiseApplicant, name = 'appointingfranchiseApplicant'),
]