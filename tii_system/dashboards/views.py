import re
import string, secrets
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from transactions.models import Transaction, TransactionTypes, Documents , Logs , MstTracking , Trackings
from django.contrib import messages

# Create your views here.
''' <------------------------- Check Attache Staff ------------------------- '''
def is_attache_staff(user):
    if user.groups.filter(name = 'attache staff').exists():
        raise PermissionDenied()
    else:
        return True
''' <---------------------- End  Check Attache Staff ----------------------> '''

''' <------------------------- Registration Code --------------------------> '''
def get_registration_code(length, choices, code):
    #<---------- Set Variable ---------->
    unique_reg_code = False
    if choices == 'letters and digits':
        string_choice = string.ascii_letters + string.digits
    elif choices == 'digits':
        string_choice = string.digits

    #<---------- Unique Registration Code ---------->
    while unique_reg_code == False:
        random      = ''.join((secrets.choice(string_choice) for i in range(length)))
        reg_code    = f'{code}-{random}'
        if not Transaction.objects.filter(registration_code = reg_code).exists():
            unique_reg_code = True

    return reg_code
''' <----------------------- End Registration Code ------------------------> '''


''' <--------------------- User Continue Submission -----------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def continue_submission(request , registration_code):
    #<---------- Get Transaction ---------->
    trans = Transaction.objects.get(registration_code = registration_code)

    #<---------- Check Status ---------->
    TRANS_STATUS = ['Draft-us-comp', 'Draft-id-comp', 'Draft-sign-comp']
    if trans.status not in TRANS_STATUS:
        raise PermissionDenied()

    #<---------- URL DISPATCHER Opening Representative ---------->
    if trans.trans_type_id.description == 'Opening Representative':

        messages.info(request, f'Continue Submission Opening Representative, Registration ID {trans.registration_code}.')

        #<---------- US Company ---------->
        if trans.status == 'Draft-us-comp':
            #<---------- Set session ---------->
            request.session['or_type']      = 'Continue Submission'
            request.session['or_trans_id']  = str(trans.trans_id)
            return redirect('transactions:openingrepresentativeUS')

        #<---------- ID Company ---------->
        if trans.status == 'Draft-id-comp':
            #<---------- Set session ---------->
            request.session['or_type']      = 'Continue Submission'
            request.session['or_trans_id']  = str(trans.trans_id)
            request.session['or_us']        = trans.status
            return redirect('transactions:openingrepresentativeUS')

        #<---------- Applicant ---------->
        if trans.status == 'Draft-sign-comp':
            #<---------- Set session ---------->
            request.session['or_type']      = 'Continue Submission'
            request.session['or_trans_id']  = str(trans.trans_id)
            request.session['or_us']        = trans.status
            request.session['or_id']        = trans.status
            return redirect('transactions:openingrepresentativeUS')

    #<---------- URL DISPATCHER Appointing Agent Distributor ---------->
    if trans.trans_type_id.description == 'Appointing Agent Distributor':

        messages.info(request, f'Continue Submission Appointing Agent Distributor Registration ID {trans.registration_code}.')

        #<---------- US Company ---------->
        if trans.status == 'Draft-us-comp':
            #<---------- Set session ---------->
            request.session['aad_type']      = 'Continue Submission'
            request.session['aad_trans_id']  = str(trans.trans_id)
            return redirect('transactions:appointingagentdistributorUS')

        # <---------- ID Company ---------->
        if trans.status == 'Draft-id-comp':
            #<---------- Set session ---------->
            request.session['aad_type']      = 'Continue Submission'
            request.session['aad_trans_id']  = str(trans.trans_id)
            request.session['aad_us']        = trans.status
            return redirect('transactions:appointingagentdistributorUS')

        #<---------- Applicant ---------->
        if trans.status == 'Draft-sign-comp':
            #<---------- Set session ---------->
            request.session['aad_type']      = 'Continue Submission'
            request.session['aad_trans_id']  = str(trans.trans_id)
            request.session['aad_us']        = trans.status
            request.session['aad_id']        = trans.status
            return redirect('transactions:appointingagentdistributorUS')

    #<---------- URL DISPATCHER Appointing Franchise ---------->
    if trans.trans_type_id.description == 'Appointing Franchise':

        messages.info(request, f'Continue Submission Appointing Franchise Registration ID {trans.registration_code}.')

        #<---------- US Company ---------->
        if trans.status == 'Draft-us-comp':
            #<---------- Set session ---------->
            request.session['af_type']      = 'Continue Submission'
            request.session['af_trans_id']  = str(trans.trans_id)
            return redirect('transactions:appointingfranchiseUS')

        #<---------- ID Company ---------->
        if trans.status == 'Draft-id-comp':
            #<---------- Set session ---------->
            request.session['af_type']      = 'Continue Submission'
            request.session['af_trans_id']  = str(trans.trans_id)
            request.session['af_us']        = trans.status
            return redirect('transactions:appointingfranchiseUS')

        #<---------- Applicant ---------->
        if trans.status == 'Draft-sign-comp':
            #<---------- Set session ---------->
            request.session['af_type']      = 'Continue Submission'
            request.session['af_trans_id']  = str(trans.trans_id)
            request.session['af_us']        = trans.status
            request.session['af_id']        = trans.status
            return redirect('transactions:appointingfranchiseUS')
''' <------------------- End User Continue Submission ---------------------> '''


''' <----------------------- User Revise Submission -----------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def revise_submission(request , registration_code):
    #<---------- Get Transaction ---------->
    trans = Transaction.objects.get(registration_code = registration_code)

    #<---------- Check Status ---------->
    TRANS_STATUS = ['Decline']
    if trans.status not in TRANS_STATUS:
        raise PermissionDenied()

    #<---------- Create Tracking  ---------->
    track = MstTracking.objects.get(name = 'revise')

    #<---------- Check Tracking  ---------->
    check_track = Trackings.objects.filter(trans_id = trans, track_id = track)
    if check_track.count() == 0:
        Trackings.objects.create(
            trans_id    = trans,
            track_id    = track
        )
    else:
        raise PermissionDenied()

    #<---------- Set Transaction Type Opening Representative ---------->
    if trans.trans_type_id.description == 'Opening Representative':

        #<---------- Set Registration Code ---------->
        new_registration_code = get_registration_code(5, 'letters and digits', 'OR')

        #<---------- Create New Transaction ---------->
        trans.pk                = None
        trans._state.adding     = True
        trans.status            = 'Draft-us-comp'
        trans.submit_date       = None
        trans.registration_code = new_registration_code
        trans.save()

        #<---------- Set session ---------->
        request.session['or_type']      = 'Revise Submission'
        request.session['or_trans_id']  = str(trans.trans_id)
        request.session['or_us']        = trans.status
        request.session['or_id']        = trans.status

        messages.info(request, f'Revision and Submission Opening Representative, Registration ID {trans.registration_code}.')

        return redirect('transactions:openingrepresentativeUS')

    #<---------- Set Transaction Type Appointing Agent Distributor ---------->
    if trans.trans_type_id.description == 'Appointing Agent Distributor':

        #<---------- Set Registration Code ---------->
        new_registration_code = get_registration_code(5, 'letters and digits', 'AD')

        #<---------- Create New Transaction ---------->
        trans.pk                = None
        trans._state.adding     = True
        trans.status            = 'Draft-us-comp'
        trans.submit_date       = None
        trans.registration_code = new_registration_code
        trans.save()

        #<---------- Set session ---------->
        request.session['aad_type']      = 'Revise Submission'
        request.session['aad_trans_id']  = str(trans.trans_id)
        request.session['aad_us']        = trans.status
        request.session['aad_id']        = trans.status

        messages.info(request, f'Revision and Submission Appointing Agent Distributor, Registration ID {trans.registration_code}.')

        return redirect('transactions:appointingagentdistributorUS')

    #<---------- Set Transaction Type Appointing Franchise ---------->
    if trans.trans_type_id.description == 'Appointing Franchise':

        #<---------- Set Registration Code ---------->
        new_registration_code = get_registration_code(5, 'letters and digits', 'AF')

        #<---------- Create New Transaction ---------->
        trans.pk                = None
        trans._state.adding     = True
        trans.status            = 'Draft-us-comp'
        trans.submit_date       = None
        trans.registration_code = new_registration_code
        trans.save()

        #<---------- Set session ---------->
        request.session['af_type']      = 'Revise Submission'
        request.session['af_trans_id']  = str(trans.trans_id)
        request.session['af_us']        = trans.status
        request.session['af_id']        = trans.status

        messages.info(request, f'Revision and Submission Appointing Franchise, Registration ID {trans.registration_code}.')

        return redirect('transactions:appointingfranchiseUS')
''' <--------------------- End User Revise Submission ---------------------> '''


''' <----------------------- User Cancel Submission -----------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def cancel_submission(request , registration_code):
    #<---------- Get Transaction ---------->
    trans = Transaction.objects.get(registration_code = registration_code)

    #<---------- Check Status ---------->
    TRANS_STATUS = ['Submit']
    if trans.status not in TRANS_STATUS:
        raise PermissionDenied()

    #<---------- Update Status transaction ---------->
    trans.status = 'Cancel'
    trans.save()

    #<---------- Create Tracking  ---------->
    track = MstTracking.objects.get(name = 'cancel')

    #<---------- Check Tracking  ---------->
    check_track = Trackings.objects.filter(trans_id = trans, track_id = track)
    if check_track.count() == 0:
        Trackings.objects.create(
            trans_id    = trans,
            track_id    = track
        )
    else:
        raise PermissionDenied()

    #<---------- Update Logs ---------->
    update_logs             = Logs.objects.get(trans_id = trans)
    update_logs.key         = 'status transaction'
    update_logs.old         = 'Submit'
    update_logs.new         = 'Cancel'
    update_logs.user_id     = int(request.user.id)
    update_logs.timestamps  = timezone.now()
    update_logs.save()

    messages.info(request, f'Registration with ID {registration_code} has been Cancelled.')

    return redirect('dashboards:detail', trans.registration_code)
''' <--------------------- End User Cancel Submission ---------------------> '''


''' <--------------------------- User Dashboard ---------------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def dashboard(request):
    return render(request, 'dashboards/udashboard.html')
''' <------------------------- End User Dashboard -------------------------> '''


''' <-------------------------- User Transaction --------------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def transaction(request):
    #<---------- Get List Transaction ---------->
    trans = Transaction.objects.filter(cid = request.user).order_by('submit_date')

    #<---------- Pagination ---------->
    page = request.GET.get('page', 1)
    paginator = Paginator(trans, 10)

    try:
        trans = paginator.page(page)
    except PageNotAnInteger :
        trans = paginator.page(1)
    except EmptyPage:
        trans = paginator.page(paginator.num_pages)

    #<---------- Render Html Context ---------->
    context = {
        'trans' : trans
    }
    return render(request, 'dashboards/utransaction.html', context)
''' <------------------------ End User Transaction ------------------------> '''


''' <---------------------- User Transaction Detail -----------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def detail(request , registration_code):
    #<---------- Get Transaction ---------->
    trans = Transaction.objects.get(registration_code = registration_code)

    #<---------- Check Status ---------->
    TRANS_STATUS = ['Draft-us-comp', 'Draft-id-comp', 'Draft-sign-comp']
    if trans.status in TRANS_STATUS:
        raise PermissionDenied()

    #<---------- Get Tracking ---------->
    track = Trackings.objects.filter(trans_id = trans)

    #<---------- Revise Process ---------->
    revise = False
    if Trackings.objects.filter(trans_id = trans, track_id__name = 'revise').exists():
        revise = True

    #<---------- Render Html Context ---------->
    context = {
        'trans' : trans,
        'track' : track,
        'revise': revise
    }

    return render(request, 'dashboards/utransactiondetail.html' , context)
''' <-------------------- End User Transaction Detail ---------------------> '''


''' <---------------------------- User Tracking ---------------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def utracking(request):
    #<---------- Title ---------->
    title = 'Transaction Tracking System'

    #<---------- Set Variable ---------->
    error_flag        = False
    error_message     = ''
    registration_code = ''
    transaction       = ''
    tracking          = ''

    #<---------- Pocess Post ---------->
    if request.method == 'POST':

        #<---------- Get Registration Code ---------->
        registration_code   = request.POST.get('registration-code')

        #<---------- Pocess Post ---------->
        if registration_code:
            if len(registration_code) < 8:
                error_flag = True
            else:
                if Transaction.objects.filter(registration_code = registration_code).exists():
                    # Check Transaction
                    transaction = Transaction.objects.get(registration_code = registration_code)
                    TRANS_STATUS = ['Draft-us-comp', 'Draft-id-comp', 'Draft-sign-comp']
                    if transaction.status in TRANS_STATUS:
                        error_message = 'Sorry, The registration code that you entered is incorrect or invalid. \
                                        please try again and remember The Registration Code are Case Sensitive.'

                    # Check Tracking
                    tracking    = Trackings.objects.filter(trans_id = transaction).order_by('timestamps')
                    if tracking.count() == 0:
                        error_message = 'Sorry, The registration code that you entered is incorrect or invalid. \
                                        please try again and remember The Registration Code are Case Sensitive.'
                else:
                    error_message = 'Sorry, The registration code that you entered is incorrect or invalid. \
                                    please try again and remember The Registration Code are Case Sensitive.'
        else:
            error_flag = True

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'transaction'       : transaction,
        'tracking'          : tracking,
        'error_flag'        : error_flag,
        'error_message'     : error_message,
        'registration_code' : registration_code
    }

    return render(request, 'dashboards/utracking.html', context)
''' <-------------------------- End User Tracking -------------------------> '''
