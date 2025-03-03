import string, secrets
from datetime import datetime, time
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from transactions.forms import Representative_Us_CompanyForm , Representative_Id_CompanyForm , \
    Agent_Distributor_Us_CompanyForm, Agent_Distributor_Id_CompanyForm, \
    Franchise_Us_CompanyForm, Franchise_Id_CompanyForm, ApplicantForm
from transactions.models import Transaction, TransactionTypes, Documents , Logs , MstTracking , Trackings

# Create your views here.
''' <------------------------ Check Attache Staff -------------------------> '''
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


''' <----------------------- Opening Representative -----------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def renewal_type_representative(request):
    #<---------- Title ---------->
    title           = 'Representative Office'
    form_title      = 'Is this a new registration?'
    form_desc_title = 'Please choose one, New Registration or Renewal.'

    #<---------- Get session ---------->
    or_type     = request.session.get('or_type')
    or_trans_id = request.session.get('or_trans_id')

    #<---------- Check session ---------->
    if or_type and or_trans_id:
        return redirect('transactions:openingrepresentativeUS')

    #<---------- Set Instance Transaction Type ---------->
    trans_type = TransactionTypes.objects.get(code = 'OR')

    #<---------- Pocess Post ---------->
    if request.method == 'POST':
        #<---------- NEW ---------->
        if request.POST.get('new'):
            #<---------- Set Registration Code ---------->
            registration_code = get_registration_code(5, 'letters and digits', 'OR')

            #<---------- Create Transaction ---------->
            trans = Transaction.objects.create(
                status              = 'Draft-us-comp',
                trans_type_id       = trans_type,
                renewal_type        = 'new',
                cid                 = request.user,
                registration_code   = registration_code
            )

            #<---------- Set session ---------->
            request.session['or_type']      = 'new'
            request.session['or_trans_id']  = str(trans.trans_id)

            return redirect('transactions:openingrepresentativeUS')

        #<---------- RE-NEW ---------->
        elif request.POST.get('renew'):
            #<--------- Set Session to Get List Transaction ----->
            request.session['or_type']          = 'renew'
            request.session['or_trans_cid']     = str(request.user)
            request.session['or_trans_type']    = str(trans_type.trans_type_id)
            request.session['or_trans_status']  = 'Complete'

            return redirect('transactions:renew_list_representative')

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
    }

    return render(request, 'transactions/trans-01-renewal.html', context)

@login_required
@user_passes_test(is_attache_staff)
def renew_list_representative(request):
    #<---------- Title ---------->
    title           = 'Representative Office'
    form_title      = 'List Transaction Completed'
    form_desc_title = 'Please choose one transaction to Renewal.'

    #<---------- Get session ---------->
    or_checked  = request.session.get('or_checked')
    or_type     = request.session.get('or_type')
    cid         = request.session.get('or_trans_cid')
    trans_type  = request.session.get('or_trans_type')
    status      = request.session.get('or_trans_status')

    #<---------- Check session ---------->
    if or_type == None:
        return redirect ('transactions:renewal_type_representative')
    if or_checked:
        return redirect('transactions:openingrepresentativeUS')

    #<---------- Get Transaction List ---------->
    trans = Transaction.objects.filter(cid = cid, trans_type_id = trans_type, status = status).order_by('submit_date')

    #<---------- Check Transaction List ---------->
    error_message = ''
    if trans.count() == 0:
        error_message = 'Sorry, At this moment you don\'t have any completed transaction for Opening Representative'
        del request.session['or_type']
        del request.session['or_trans_cid']
        del request.session['or_trans_type']
        del request.session['or_trans_status']

    #<---------- Pagination ---------->
    page = request.GET.get('page', 1)
    paginator = Paginator(trans, 10)

    try:
        trans = paginator.page(page)
    except PageNotAnInteger :
        trans = paginator.page(1)
    except EmptyPage:
        trans = paginator.page(paginator.num_pages)

    #<---------- Pocess Post ---------->
    if request.method == 'POST':
        transaction = request.POST

        id_transaction = ''
        for key, value in transaction.items():
            if 'transaction_' in key:
                id_transaction = value

        #<---------- Get Transaction ---------->
        get_trans = Transaction.objects.get(trans_id = id_transaction)

        #<---------- Set Registration Code ---------->
        registration_code = get_registration_code(5, 'letters and digits', 'OR')

        #<---------- Create New Transaction ---------->
        get_trans.pk                = None
        get_trans._state.adding     = True
        get_trans.status            = 'Draft-us-comp'
        get_trans.submit_date       = None
        get_trans.renewal_type      = 'renew'
        get_trans.registration_code = registration_code
        get_trans.save()

        #<---------- Set session ---------->
        request.session['or_checked']   = str(get_trans.trans_id)
        request.session['or_trans_id']  = str(get_trans.trans_id)
        request.session['or_us']        = get_trans.status
        request.session['or_id']        = get_trans.status
        request.session['or_app']       = get_trans.status

        return redirect('transactions:openingrepresentativeUS')

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
        'error_message'     : error_message,
        'trans'             : trans
    }

    return render(request, 'transactions/trans-02-renew-list.html', context)

@login_required
@user_passes_test(is_attache_staff)
def openingrepresentativeUS(request):
    #<---------- Title ---------->
    title           = 'Representative Office'
    form_title      = 'STATEMENT OF XA COMPANY DESIRING TO HAVE A REPRESENTATIVE OFFICE IN XB'
    form_desc_title = 'This is to state that the following information is to appoint and/or opening a representative office in XB:'

    #<---------- Get session ---------->
    or_type     = request.session.get('or_type')
    or_trans_id = request.session.get('or_trans_id')
    or_us       = request.session.get('or_us')

    #<---------- Check session ---------->
    if or_type == None and or_trans_id == None:
        return redirect ('transactions:renewal_type_representative')
    if or_us == None:
        #<---------- Pocess Post ---------->
        user = Transaction.objects.get(trans_id = or_trans_id)
        if request.method == 'POST':
            form = Representative_Us_CompanyForm(request.POST, request.FILES)
            if form.is_valid():
                user.comp_us_name           = form.cleaned_data['comp_us_name']
                user.comp_us_president      = form.cleaned_data['comp_us_president']
                user.comp_us_legal_status   = form.cleaned_data['comp_us_legal_status']
                user.comp_us_establishment  = form.cleaned_data['comp_us_establishment']
                user.comp_us_address        = form.cleaned_data['comp_us_address']
                user.comp_us_state          = form.cleaned_data['comp_us_state']
                user.comp_us_city           = form.cleaned_data['comp_us_city']
                user.comp_us_zip            = form.cleaned_data['comp_us_zip']
                user.comp_us_website        = form.cleaned_data['comp_us_website']
                user.comp_us_phone          = form.cleaned_data['comp_us_phone']
                user.comp_us_fax            = form.cleaned_data['comp_us_fax']
                user.comp_us_email          = form.cleaned_data['comp_us_email']
                user.line_of_business       = form.cleaned_data['line_of_business']
                user.product_offering       = form.cleaned_data['product_offering']
                user.cert_good_standing     = form.cleaned_data['cert_good_standing']
                user.status                 = 'Draft-id-comp'
                user.save()

                #<---------- Set session ---------->
                request.session['or_us'] = user.status

                return redirect('transactions:openingrepresentativeID')

        else:
            form = Representative_Us_CompanyForm()

    if or_us:
        #<---------- Pocess Post with populated data ---------->
        populated_data = Transaction.objects.get(trans_id = or_trans_id)
        if request.method == 'POST':
            form = Representative_Us_CompanyForm(request.POST, request.FILES, instance = populated_data)
            if form.is_valid():
                populated_data.comp_us_name           = form.cleaned_data['comp_us_name']
                populated_data.comp_us_president      = form.cleaned_data['comp_us_president']
                populated_data.comp_us_legal_status   = form.cleaned_data['comp_us_legal_status']
                populated_data.comp_us_establishment  = form.cleaned_data['comp_us_establishment']
                populated_data.comp_us_address        = form.cleaned_data['comp_us_address']
                populated_data.comp_us_state          = form.cleaned_data['comp_us_state']
                populated_data.comp_us_city           = form.cleaned_data['comp_us_city']
                populated_data.comp_us_zip            = form.cleaned_data['comp_us_zip']
                populated_data.comp_us_website        = form.cleaned_data['comp_us_website']
                populated_data.comp_us_phone          = form.cleaned_data['comp_us_phone']
                populated_data.comp_us_fax            = form.cleaned_data['comp_us_fax']
                populated_data.comp_us_email          = form.cleaned_data['comp_us_email']
                populated_data.line_of_business       = form.cleaned_data['line_of_business']
                populated_data.product_offering       = form.cleaned_data['product_offering']
                populated_data.cert_good_standing     = form.cleaned_data['cert_good_standing']
                populated_data.status                 = 'Draft-id-comp'
                populated_data.save()

                return redirect('transactions:openingrepresentativeID')

        else:
            form = Representative_Us_CompanyForm(instance = populated_data)

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
        'form'              : form
    }

    return render(request, 'transactions/trans-03-us-company-representative.html', context)

@login_required
@user_passes_test(is_attache_staff)
def openingrepresentativeID(request):
    #<---------- Title ---------->
    title           = 'Representative Office'
    form_title      = 'STATEMENT OF XA COMPANY DESIRING TO HAVE A REPRESENTATIVE OFFICE IN XB'
    form_desc_title = 'This is to state that the following information is to appoint and/or opening a representative office in XB:'

    #<---------- Get session ---------->
    or_type     = request.session.get('or_type')
    or_trans_id = request.session.get('or_trans_id')
    or_us       = request.session.get('or_us')
    or_id       = request.session.get('or_id')

    #<---------- Check session ---------->
    if or_type == None and or_trans_id == None:
        return redirect ('transactions:renewal_type_representative')
    if or_us == None:
        return redirect ('transactions:openingrepresentativeUS')
    if or_id == None:
        #<---------- Pocess Post ---------->
        user = Transaction.objects.get(trans_id = or_trans_id)
        if request.method == 'POST':
            form = Representative_Id_CompanyForm(request.POST, request.FILES)
            if form.is_valid():
                user.comp_idn_name          = form.cleaned_data['comp_idn_name']
                user.comp_idn_president     = form.cleaned_data['comp_idn_president']
                user.comp_idn_address       = form.cleaned_data['comp_idn_address']
                user.comp_idn_province      = form.cleaned_data['comp_idn_province']
                user.comp_idn_city          = form.cleaned_data['comp_idn_city']
                user.comp_idn_zip           = form.cleaned_data['comp_idn_zip']
                user.comp_idn_website       = form.cleaned_data['comp_idn_website']
                user.comp_idn_phone         = form.cleaned_data['comp_idn_phone']
                user.comp_idn_fax           = form.cleaned_data['comp_idn_fax']
                user.comp_idn_email         = form.cleaned_data['comp_idn_email']
                user.term                   = form.cleaned_data['term']
                user.term_unit              = form.cleaned_data['term_unit']
                user.comp_idn_nationality   = form.cleaned_data['comp_idn_nationality']
                user.comp_idn_idnumber      = form.cleaned_data['comp_idn_idnumber']
                user.comp_idn_rep_officer   = form.cleaned_data['comp_idn_rep_officer']
                user.loi                    = form.cleaned_data['loi']
                user.loa                    = form.cleaned_data['loa']
                user.los                    = form.cleaned_data['los']
                user.status                 = 'Draft-sign-comp'
                user.save()

                #<---------- Set session ---------->
                request.session['or_id'] = user.status

                return redirect('transactions:openingrepresentativeApplicant')

        else:
            form = Representative_Id_CompanyForm()

    if or_id:
        #<---------- Pocess Post with populated data ---------->
        populated_data = Transaction.objects.get(trans_id = or_trans_id)

        if request.method == 'POST':
            form = Representative_Id_CompanyForm(request.POST, request.FILES, instance = populated_data)
            if form.is_valid():
                populated_data.comp_idn_name          = form.cleaned_data['comp_idn_name']
                populated_data.comp_idn_president     = form.cleaned_data['comp_idn_president']
                populated_data.comp_idn_address       = form.cleaned_data['comp_idn_address']
                populated_data.comp_idn_province      = form.cleaned_data['comp_idn_province']
                populated_data.comp_idn_city          = form.cleaned_data['comp_idn_city']
                populated_data.comp_idn_zip           = form.cleaned_data['comp_idn_zip']
                populated_data.comp_idn_website       = form.cleaned_data['comp_idn_website']
                populated_data.comp_idn_phone         = form.cleaned_data['comp_idn_phone']
                populated_data.comp_idn_fax           = form.cleaned_data['comp_idn_fax']
                populated_data.comp_idn_email         = form.cleaned_data['comp_idn_email']
                populated_data.term                   = form.cleaned_data['term']
                populated_data.term_unit              = form.cleaned_data['term_unit']
                populated_data.comp_idn_nationality   = form.cleaned_data['comp_idn_nationality']
                populated_data.comp_idn_idnumber      = form.cleaned_data['comp_idn_idnumber']
                populated_data.comp_idn_rep_officer   = form.cleaned_data['comp_idn_rep_officer']
                populated_data.loi                    = form.cleaned_data['loi']
                populated_data.loa                    = form.cleaned_data['loa']
                populated_data.los                    = form.cleaned_data['los']
                populated_data.status                 = 'Draft-sign-comp'
                populated_data.save()

                return redirect('transactions:openingrepresentativeApplicant')

        else:
            form = Representative_Id_CompanyForm(instance = populated_data)

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
        'form'              : form
    }

    return render(request, 'transactions/trans-04-id-company-representative.html', context)

@login_required
@user_passes_test(is_attache_staff)
def openingrepresentativeApplicant(request):
    #<---------- Title ---------->
    title           = 'Representative Office'
    form_title      = 'STATEMENT OF XA COMPANY DESIRING TO HAVE A REPRESENTATIVE OFFICE IN XB'
    form_desc_title = 'This is to state that the following information is to appoint and/or opening a representative office in XB:'

    #<---------- Get session ---------->
    or_type     = request.session.get('or_type')
    or_trans_id = request.session.get('or_trans_id')
    or_us       = request.session.get('or_us')
    or_id       = request.session.get('or_id')
    or_app      = request.session.get('or_app')

    #<---------- Check session ---------->
    if or_type == None and or_trans_id == None:
        return redirect ('transactions:renewal_type_representative')
    if or_us == None:
        return redirect ('transactions:openingrepresentativeUS')
    if or_id == None:
        return redirect ('transactions:openingrepresentativeID')
    if or_app == None:
        #<---------- Pocess Post ---------->
        user = Transaction.objects.get(trans_id = or_trans_id)
        if request.method == 'POST':
            form = ApplicantForm(request.POST, request.FILES)
            if form.is_valid():
                #<---------- Set Date ---------->
                datenow = timezone.now()

                #<---------- Save to table transaction ---------->
                user.applicant_name     = form.cleaned_data['applicant_name']
                user.applicant_position = form.cleaned_data['applicant_position']
                user.applicant_city     = form.cleaned_data['applicant_city']
                user.submit_date        = datenow
                user.status             = 'Submit'
                user.save()

                #<---------- Create Tracking ---------->
                track = MstTracking.objects.get(name = 'submitted')
                Trackings.objects.create(
                    trans_id    = user,
                    track_id    = track
                )

                #<---------- Create Logs ---------->
                Logs.objects.create(
                    trans_id    = user,
                    key         = 'status transaction',
                    old         = 'None',
                    new         = 'Submit',
                    user_id     = request.user.id,
                    timestamps  = datenow
                )

                #<---------- Delete transaction session ---------->
                del request.session['or_trans_id']
                del request.session['or_type']
                del request.session['or_us']
                del request.session['or_id']

                return redirect('dashboards:dashboard')

        else:
            form = ApplicantForm()

    if or_app:
        #<---------- Pocess Post with populated data ---------->
        populated_data = Transaction.objects.get(trans_id = or_trans_id)
        if request.method == 'POST':
            form = ApplicantForm(request.POST, request.FILES, instance = populated_data)
            if form.is_valid():
                #<---------- Set Date ---------->
                datenow = timezone.now()

                #<---------- Save to table transaction ---------->
                populated_data.applicant_name     = form.cleaned_data['applicant_name']
                populated_data.applicant_position = form.cleaned_data['applicant_position']
                populated_data.applicant_city     = form.cleaned_data['applicant_city']
                populated_data.submit_date        = datenow
                populated_data.status             = 'Submit'
                populated_data.save()

                #<---------- Create Tracking ---------->
                track = MstTracking.objects.get(name = 'submitted')
                Trackings.objects.create(
                    trans_id    = populated_data,
                    track_id    = track
                )

                #<---------- Create Logs ---------->
                Logs.objects.create(
                    trans_id    = populated_data,
                    key         = 'status transaction',
                    old         = 'None',
                    new         = 'Submit',
                    user_id     = request.user.id,
                    timestamps  = datenow
                )

                #<---------- Delete transaction session ---------->
                del request.session['or_trans_id']
                del request.session['or_type']
                del request.session['or_us']
                del request.session['or_id']
                del request.session['or_app']
                del request.session['or_trans_cid']
                del request.session['or_trans_type']
                del request.session['or_trans_status']
                del request.session['or_checked']

                return redirect('dashboards:dashboard')

        else:
            form = ApplicantForm(instance = populated_data)

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
        'form'              : form
    }

    return render(request, 'transactions/trans-05-applicant.html', context)
''' <--------------------- END Opening Representative ---------------------> '''


''' <-------------------- Appointing Agent Distributor --------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def renewal_type_agentdistributor(request):
    #<---------- Title ---------->
    title           = 'Appointing Agent or Distributor'
    form_title      = 'Is this a new registration?'
    form_desc_title = 'Please choose one, New Registration or Renewal.'

    #<------------ Get session ---------->
    aad_type        = request.session.get('or_type')
    aad_trans_id    = request.session.get('aad_trans_id')

    #<---------- Check session ---------->
    if aad_type and aad_trans_id:
        return redirect('transactions:appointingagentdistributorUS')

    #<---------- Set Instance Transaction Type ---------->
    trans_type = TransactionTypes.objects.get(code = 'AAD')

    #<---------- Pocess Post ---------->
    if request.method == 'POST':
        #<---------- NEW ---------->
        if request.POST.get('new'):
            #<---------- Set Registration Code ---------->
            registration_code = get_registration_code(5, 'letters and digits', 'AD')

            #<---------- Create Transaction ---------->
            trans = Transaction.objects.create(
                status              = 'Draft-us-comp',
                trans_type_id       = trans_type,
                renewal_type        = 'new',
                cid                 = request.user,
                registration_code   = registration_code
            )

            #<---------- Set session ---------->
            request.session['aad_type']     = 'new'
            request.session['aad_trans_id'] = str(trans.trans_id)

            return redirect('transactions:appointingagentdistributorUS')

        #<---------- RE-NEW ---------->
        elif request.POST.get('renew'):
            #<--------- Set Session to Get List Transaction ----->
            request.session['aad_type']         = 'renew'
            request.session['aad_trans_cid']    = str(request.user)
            request.session['aad_trans_type']   = str(trans_type.trans_type_id)
            request.session['aad_trans_status'] = 'Complete'

            return redirect('transactions:renew_list_agentdistributor')

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
    }

    return render(request, 'transactions/trans-01-renewal.html', context)

@login_required
@user_passes_test(is_attache_staff)
def renew_list_agentdistributor(request):
    #<---------- Title ---------->
    title           = 'Appointing Agent or Distributor'
    form_title      = 'List Transaction Completed'
    form_desc_title = 'Please choose one transaction to Renewal.'

    #<---------- Get session ---------->
    aad_check   = request.session.get('aad_checked')
    aad_type    = request.session.get('aad_type')
    cid         = request.session.get('aad_trans_cid')
    trans_type  = request.session.get('aad_trans_type')
    status      = request.session.get('aad_trans_status')

    #<---------- Check session ---------->
    if aad_type == None:
        return redirect ('transactions:renewal_type_agentdistributor')
    if aad_check:
        return redirect('transactions:appointingagentdistributorUS')

    #<---------- Get Transaction List ---------->
    trans = Transaction.objects.filter(cid = cid, trans_type_id = trans_type, status = status).order_by('submit_date')

    #<---------- Check Transaction List ---------->
    error_message = ''
    if trans.count() == 0:
        error_message = 'Sorry, At this moment you don\'t have any completed transaction for Appointing Agent or Distributor'
        del request.session['aad_type']
        del request.session['aad_trans_cid']
        del request.session['aad_trans_type']
        del request.session['aad_trans_status']

    #<---------- Pagination ---------->
    page = request.GET.get('page', 1)
    paginator = Paginator(trans, 10)

    try:
        trans = paginator.page(page)
    except PageNotAnInteger :
        trans = paginator.page(1)
    except EmptyPage:
        trans = paginator.page(paginator.num_pages)

    #<---------- Pocess Post ---------->
    if request.method == 'POST':
        transaction = request.POST

        id_transaction = ''
        for key, value in transaction.items():
            if 'transaction_' in key:
                id_transaction = value

        #<---------- Get Transaction ---------->
        get_trans = Transaction.objects.get(trans_id = id_transaction)

        #<---------- Set Registration Code ---------->
        registration_code = get_registration_code(5, 'letters and digits', 'AD')

        #<---------- Create New Transaction ---------->
        get_trans.pk                = None
        get_trans._state.adding     = True
        get_trans.status            = 'Draft-us-comp'
        get_trans.submit_date       = None
        get_trans.renewal_type      = 'renew'
        get_trans.registration_code = registration_code
        get_trans.save()

        #<---------- Set session ---------->
        request.session['aad_checked']  = str(get_trans.trans_id)
        request.session['aad_trans_id'] = str(get_trans.trans_id)
        request.session['aad_us']       = get_trans.status
        request.session['aad_id']       = get_trans.status
        request.session['aad_app']      = get_trans.status

        return redirect('transactions:appointingagentdistributorUS')

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
        'error_message'     : error_message,
        'trans'             : trans
    }

    return render(request , 'transactions/trans-02-renew-list.html', context)

@login_required
@user_passes_test(is_attache_staff)
def appointingagentdistributorUS(request):
    #<---------- Title ---------->
    title           = 'Appointing Agent or Distributor'
    form_title      = 'STATEMENT OF XA COMPANY DESIRING TO HAVE SALES AGENT, OR, DISTRIBUTOR IN XB'
    form_desc_title = 'This is to state that the following information is to appoint a sales agent, or distributor in XB:'

    #<---------- Get session ---------->
    aad_type    = request.session.get('aad_type')
    aad_trans_id= request.session.get('aad_trans_id')
    aad_us      = request.session.get('aad_us')

    #<---------- Check session ---------->
    if aad_type == None and aad_trans_id == None:
        return redirect ('transactions:renewal_type_agentdistributor')
    if aad_us == None:
        #<---------- Pocess Post ---------->
        user = Transaction.objects.get(trans_id = aad_trans_id)
        if request.method == 'POST':
            form = Agent_Distributor_Us_CompanyForm(request.POST, request.FILES)
            if form.is_valid():
                user.comp_us_name           = form.cleaned_data['comp_us_name']
                user.comp_us_president      = form.cleaned_data['comp_us_president']
                user.comp_us_legal_status   = form.cleaned_data['comp_us_legal_status']
                user.comp_us_establishment  = form.cleaned_data['comp_us_establishment']
                user.comp_us_address        = form.cleaned_data['comp_us_address']
                user.comp_us_state          = form.cleaned_data['comp_us_state']
                user.comp_us_city           = form.cleaned_data['comp_us_city']
                user.comp_us_zip            = form.cleaned_data['comp_us_zip']
                user.comp_us_website        = form.cleaned_data['comp_us_website']
                user.comp_us_phone          = form.cleaned_data['comp_us_phone']
                user.comp_us_fax            = form.cleaned_data['comp_us_fax']
                user.comp_us_email          = form.cleaned_data['comp_us_email']
                user.line_of_business       = form.cleaned_data['line_of_business']
                user.product_offering       = form.cleaned_data['product_offering']
                user.hs_code                = form.cleaned_data['hs_code']
                user.cert_good_standing     = form.cleaned_data['cert_good_standing']
                user.status                 = 'Draft-id-comp'
                user.save()

                #<---------- Set session ---------->
                request.session['aad_us'] = user.status

                return redirect('transactions:appointingagentdistributorID')

        else:
            form = Agent_Distributor_Us_CompanyForm()

    if aad_us:
        #<---------- Pocess Post with populated data ---------->
        populated_data = Transaction.objects.get(trans_id = aad_trans_id)
        if request.method == 'POST':
            form = Agent_Distributor_Us_CompanyForm(request.POST, request.FILES, instance = populated_data)
            if form.is_valid():
                populated_data.comp_us_name           = form.cleaned_data['comp_us_name']
                populated_data.comp_us_president      = form.cleaned_data['comp_us_president']
                populated_data.comp_us_legal_status   = form.cleaned_data['comp_us_legal_status']
                populated_data.comp_us_establishment  = form.cleaned_data['comp_us_establishment']
                populated_data.comp_us_address        = form.cleaned_data['comp_us_address']
                populated_data.comp_us_state          = form.cleaned_data['comp_us_state']
                populated_data.comp_us_city           = form.cleaned_data['comp_us_city']
                populated_data.comp_us_zip            = form.cleaned_data['comp_us_zip']
                populated_data.comp_us_website        = form.cleaned_data['comp_us_website']
                populated_data.comp_us_phone          = form.cleaned_data['comp_us_phone']
                populated_data.comp_us_fax            = form.cleaned_data['comp_us_fax']
                populated_data.comp_us_email          = form.cleaned_data['comp_us_email']
                populated_data.line_of_business       = form.cleaned_data['line_of_business']
                populated_data.product_offering       = form.cleaned_data['product_offering']
                populated_data.hs_code                = form.cleaned_data['hs_code']
                populated_data.cert_good_standing     = form.cleaned_data['cert_good_standing']
                populated_data.status                 = 'Draft-id-comp'
                populated_data.save()

                return redirect('transactions:appointingagentdistributorID')

        else:
            form = Agent_Distributor_Us_CompanyForm(instance = populated_data)


    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
        'form'              : form
    }

    return render(request,'transactions/trans-03-us-company-agentdistributor.html', context)

@login_required
@user_passes_test(is_attache_staff)
def appointingagentdistributorID(request):
    #<---------- Title ---------->
    title           = 'Appointing Agent or Distributor'
    form_title      = 'STATEMENT OF XA COMPANY DESIRING TO HAVE SALES AGENT, OR, DISTRIBUTOR IN XB'
    form_desc_title = 'This is to state that the following information is to appoint a sales agent, or distributor in XB:'

    #<---------- Get session ---------->
    aad_type    = request.session.get('aad_type')
    aad_trans_id= request.session.get('aad_trans_id')
    aad_us      = request.session.get('aad_us')
    aad_id      = request.session.get('aad_id')

    #<---------- Check session ---------->
    if aad_type == None and aad_trans_id == None:
        return redirect ('transactions:renewal_type_agentdistributor')
    if aad_us == None:
        return redirect('transactions:appointingagentdistributorUS')
    if aad_id == None:
        #<---------- Pocess Post ---------->
        user = Transaction.objects.get(trans_id = aad_trans_id)
        if request.method == 'POST':
            form = Agent_Distributor_Id_CompanyForm(request.POST, request.FILES)
            if form.is_valid():
                user.comp_idn_name          = form.cleaned_data['comp_idn_name']
                user.comp_idn_president     = form.cleaned_data['comp_idn_president']
                user.comp_idn_address       = form.cleaned_data['comp_idn_address']
                user.comp_idn_province      = form.cleaned_data['comp_idn_province']
                user.comp_idn_city          = form.cleaned_data['comp_idn_city']
                user.comp_idn_zip           = form.cleaned_data['comp_idn_zip']
                user.comp_idn_website       = form.cleaned_data['comp_idn_website']
                user.comp_idn_phone         = form.cleaned_data['comp_idn_phone']
                user.comp_idn_fax           = form.cleaned_data['comp_idn_fax']
                user.comp_idn_email         = form.cleaned_data['comp_idn_email']
                user.term                   = form.cleaned_data['term']
                user.term_unit              = form.cleaned_data['term_unit']
                user.comp_idn_nationality   = form.cleaned_data['comp_idn_nationality']
                user.comp_idn_idnumber      = form.cleaned_data['comp_idn_idnumber']
                user.comp_idn_rep_officer   = form.cleaned_data['comp_idn_rep_officer']
                user.contractual_agreement  = form.cleaned_data['contractual_agreement']
                user.status                 = 'Draft-sign-comp'
                user.save()

                #<---------- Set session ---------->
                request.session['aad_id'] = user.status

                return redirect('transactions:appointingagentdistributorApplicant')

        else:
            form = Agent_Distributor_Id_CompanyForm()

    if aad_id:
        #<---------- Pocess Post with populated data ---------->
        populated_data = Transaction.objects.get(trans_id = aad_trans_id)
        if request.method == 'POST':
            form = Agent_Distributor_Id_CompanyForm(request.POST, request.FILES, instance = populated_data)
            if form.is_valid():
                populated_data.comp_idn_name          = form.cleaned_data['comp_idn_name']
                populated_data.comp_idn_president     = form.cleaned_data['comp_idn_president']
                populated_data.comp_idn_address       = form.cleaned_data['comp_idn_address']
                populated_data.comp_idn_province      = form.cleaned_data['comp_idn_province']
                populated_data.comp_idn_city          = form.cleaned_data['comp_idn_city']
                populated_data.comp_idn_zip           = form.cleaned_data['comp_idn_zip']
                populated_data.comp_idn_website       = form.cleaned_data['comp_idn_website']
                populated_data.comp_idn_phone         = form.cleaned_data['comp_idn_phone']
                populated_data.comp_idn_fax           = form.cleaned_data['comp_idn_fax']
                populated_data.comp_idn_email         = form.cleaned_data['comp_idn_email']
                populated_data.term                   = form.cleaned_data['term']
                populated_data.term_unit              = form.cleaned_data['term_unit']
                populated_data.comp_idn_nationality   = form.cleaned_data['comp_idn_nationality']
                populated_data.comp_idn_idnumber      = form.cleaned_data['comp_idn_idnumber']
                populated_data.comp_idn_rep_officer   = form.cleaned_data['comp_idn_rep_officer']
                populated_data.contractual_agreement  = form.cleaned_data['contractual_agreement']
                populated_data.status                 = 'Draft-sign-comp'
                populated_data.save()

                return redirect('transactions:appointingagentdistributorApplicant')

        else:
            form = Agent_Distributor_Id_CompanyForm(instance = populated_data)

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
        'form'              : form
    }

    return render(request,'transactions/trans-04-id-company-agentdistributor.html', context)

@login_required
@user_passes_test(is_attache_staff)
def appointingagentdistributorApplicant(request):
    #<---------- Title ---------->
    title           = 'Appointing Agent or Distributor'
    form_title      = 'STATEMENT OF XA COMPANY DESIRING TO HAVE SALES AGENT, OR, DISTRIBUTOR IN XB'
    form_desc_title = 'This is to state that the following information is to appoint a sales agent, or distributor in XB:'

    #<---------- Get session ---------->
    aad_type    = request.session.get('aad_type')
    aad_trans_id= request.session.get('aad_trans_id')
    aad_us      = request.session.get('aad_us')
    aad_id      = request.session.get('aad_id')
    aad_app     = request.session.get('aad_app')

    #<---------- Check session ---------->
    if aad_type == None and aad_trans_id == None:
        return redirect ('transactions:renewal_type_agentdistributor')
    if aad_us == None:
        return redirect ('transactions:appointingagentdistributorUS')
    if aad_id == None:
        return redirect ('transactions:appointingagentdistributorID')
    if aad_app == None:
        #<---------- Pocess Post ---------->
        user = Transaction.objects.get(trans_id = aad_trans_id)
        if request.method == 'POST':
            form = ApplicantForm(request.POST, request.FILES)
            if form.is_valid():
                #<---------- Set Date ---------->
                datenow = timezone.now()

                #<---------- Save to table transaction ---------->
                user.applicant_name     = form.cleaned_data['applicant_name']
                user.applicant_position = form.cleaned_data['applicant_position']
                user.applicant_city     = form.cleaned_data['applicant_city']
                user.submit_date        = datenow
                user.status             = 'Submit'
                user.save()

                #<---------- Create Tracking ---------->
                track = MstTracking.objects.get(name = 'submitted')
                Trackings.objects.create(
                    trans_id    = user,
                    track_id    = track
                )

                #<---------- Create Logs ---------->
                Logs.objects.create(
                    trans_id    = user,
                    key         = 'status transaction',
                    old         = 'None',
                    new         = 'Submit',
                    user_id     = request.user.id,
                    timestamps  = datenow
                )

                #<---------- Delete transaction session ---------->
                del request.session['aad_trans_id']
                del request.session['aad_type']
                del request.session['aad_us']
                del request.session['aad_id']

                return redirect('dashboards:dashboard')

        else:
            form = ApplicantForm()

    if aad_app:
        #<---------- Pocess Post with populated data ---------->
        populated_data = Transaction.objects.get(trans_id = aad_trans_id)
        if request.method == 'POST':
            form = ApplicantForm(request.POST, request.FILES, instance = populated_data)
            if form.is_valid():
                #<---------- Set Date ---------->
                datenow = timezone.now()

                #<---------- Save to table transaction ---------->
                populated_data.applicant_name     = form.cleaned_data['applicant_name']
                populated_data.applicant_position = form.cleaned_data['applicant_position']
                populated_data.applicant_city     = form.cleaned_data['applicant_city']
                populated_data.submit_date        = datenow
                populated_data.status             = 'Submit'
                populated_data.save()

                #<---------- Create Tracking ---------->
                track = MstTracking.objects.get(name = 'submitted')
                Trackings.objects.create(
                    trans_id    = populated_data,
                    track_id    = track
                )

                #<---------- Create Logs ---------->
                Logs.objects.create(
                    trans_id    = populated_data,
                    key         = 'status transaction',
                    old         = 'None',
                    new         = 'Submit',
                    user_id     = request.user.id,
                    timestamps  = datenow
                )

                #<---------- Delete transaction session ---------->
                del request.session['aad_trans_id']
                del request.session['aad_type']
                del request.session['aad_us']
                del request.session['aad_id']
                del request.session['aad_app']
                del request.session['aad_trans_cid']
                del request.session['aad_trans_type']
                del request.session['aad_trans_status']
                del request.session['aad_checked']

                return redirect('dashboards:dashboard')
        else:
            form = ApplicantForm(instance = populated_data)

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
        'form'              : form
    }

    return render(request,'transactions/trans-05-applicant.html', context)
''' <------------------ END Appointing Agent Distributor ------------------> '''


''' <------------------------ Appointing Franchise ------------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def renewal_type_franchise(request):
    #<---------- Title ---------->
    title           = 'Franchise'
    form_title      = 'Is this a new registration?'
    form_desc_title = 'Please choose one, New Registration or Renewal.'

    #<------------ Get session ---------->
    af_type     = request.session.get('af_type')
    af_trans_id = request.session.get('af_trans_id')

    #<---------- Check session ---------->
    if af_type and af_trans_id:
        return redirect('transactions:appointingfranchiseUS')

    #<---------- Set Instance ---------->
    trans_type = TransactionTypes.objects.get(code = 'AF')

    #<---------- Pocess Post ---------->
    if request.method == 'POST':
        #<---------- NEW ---------->
        if request.POST.get('new'):
            #<---------- Set Registration Code ---------->
            registration_code = get_registration_code(5, 'letters and digits', 'AF')

            #<---------- Create Transaction ---------->
            trans = Transaction.objects.create(
                status              = 'Draft-us-comp',
                trans_type_id       = trans_type,
                renewal_type        = 'new',
                cid                 = request.user,
                registration_code   = registration_code
            )

            #<---------- Set session ---------->
            request.session['af_type']      = 'new'
            request.session['af_trans_id']  = str(trans.trans_id)

            return redirect('transactions:appointingfranchiseUS')

        #<---------- RE-NEW ---------->
        elif request.POST.get('renew'):
            #<--------- Set Session to Get List Transaction ----->
            request.session['af_type']          = 'renew'
            request.session['af_trans_cid']     = str(request.user)
            request.session['af_trans_type']    = str(trans_type.trans_type_id)
            request.session['af_trans_status']  = 'Complete'

            return redirect('transactions:renew_list_franchise')

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
    }

    return render(request, 'transactions/trans-01-renewal.html', context)

@login_required
@user_passes_test(is_attache_staff)
def renew_list_franchise(request):
    #<---------- Title ---------->
    title           = 'Franchise'
    form_title      = 'List Transaction Completed'
    form_desc_title = 'Please choose one transaction to Renewal.'

    #<---------- Get session ---------->
    af_check    = request.session.get('af_checked')
    af_type     = request.session.get('af_type')
    cid         = request.session.get('af_trans_cid')
    trans_type  = request.session.get('af_trans_type')
    status      = request.session.get('af_trans_status')

    #<---------- Check session ---------->
    if af_type == None:
        return redirect ('transactions:renewal_type_franchise')
    if af_check:
        return redirect('transactions:appointingfranchiseUS')

    #<---------- Get Transaction List ---------->
    trans = Transaction.objects.filter(cid = cid, trans_type_id = trans_type, status = status).order_by('submit_date')

    #<---------- Check Transaction List ---------->
    error_message = ''
    if trans.count() == 0:
        error_message = 'Sorry, At this moment you don\'t have any completed transaction for Appointing Franchise'
        del request.session['af_type']
        del request.session['af_trans_cid']
        del request.session['af_trans_type']
        del request.session['af_trans_status']

    #<---------- Pagination ---------->
    page = request.GET.get('page', 1)
    paginator = Paginator(trans, 10)

    try:
        trans = paginator.page(page)
    except PageNotAnInteger :
        trans = paginator.page(1)
    except EmptyPage:
        trans = paginator.page(paginator.num_pages)

    #<---------- Pocess Post ---------->
    if request.method == 'POST':
        transaction = request.POST

        id_transaction = ''
        for key, value in transaction.items():
            if 'transaction_' in key:
                id_transaction = value

        #<---------- Get Transaction ---------->
        get_trans = Transaction.objects.get(trans_id = id_transaction)

        #<---------- Set Registration Code ---------->
        registration_code = get_registration_code(5, 'letters and digits', 'AF')

        #<---------- Create New Transaction ---------->
        get_trans.pk                = None
        get_trans._state.adding     = True
        get_trans.status            = 'Draft-us-comp'
        get_trans.submit_date       = None
        get_trans.renewal_type      = 'renew'
        get_trans.registration_code = registration_code
        get_trans.save()

        #<---------- Set session ---------->
        request.session['af_checked']   = str(get_trans.trans_id)
        request.session['af_trans_id']  = str(get_trans.trans_id)
        request.session['af_us']        = get_trans.status
        request.session['af_id']        = get_trans.status
        request.session['af_app']       = get_trans.status

        return redirect('transactions:appointingfranchiseUS')

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
        'error_message'     : error_message,
        'trans'             : trans
    }

    return render(request , 'transactions/trans-02-renew-list.html', context)

@login_required
@user_passes_test(is_attache_staff)
def appointingfranchiseUS(request):
    #<---------- Title ---------->
    title           = 'Franchise'
    form_title      = 'STATEMENT OF XA COMPANY DESIRING TO REGISTER A FRENCHISE BUSINESS IN XB'
    form_desc_title = 'This is to state that the following information is to appoint a representative, sales agent, or distributor in XB:'

    #<---------- Get session ---------->
    af_type     = request.session.get('af_type')
    af_trans_id = request.session.get('af_trans_id')
    af_us       = request.session.get('af_us')

    #<---------- Check session ---------->
    if af_type == None and af_trans_id == None:
        return redirect('transactions:renewal_type_franchise')
    if af_us == None:
        #<---------- Pocess Post ---------->
        user = Transaction.objects.get(trans_id = af_trans_id)
        if request.method == 'POST':
            form = Franchise_Us_CompanyForm(request.POST, request.FILES)
            if form.is_valid():
                user.comp_us_name           = form.cleaned_data['comp_us_name']
                user.comp_us_president      = form.cleaned_data['comp_us_president']
                user.comp_us_legal_status   = form.cleaned_data['comp_us_legal_status']
                user.comp_us_establishment  = form.cleaned_data['comp_us_establishment']
                user.comp_us_address        = form.cleaned_data['comp_us_address']
                user.comp_us_state          = form.cleaned_data['comp_us_state']
                user.comp_us_city           = form.cleaned_data['comp_us_city']
                user.comp_us_zip            = form.cleaned_data['comp_us_zip']
                user.comp_us_website        = form.cleaned_data['comp_us_website']
                user.comp_us_phone          = form.cleaned_data['comp_us_phone']
                user.comp_us_fax            = form.cleaned_data['comp_us_fax']
                user.comp_us_email          = form.cleaned_data['comp_us_email']
                user.line_of_business       = form.cleaned_data['line_of_business']
                user.product_offering       = form.cleaned_data['product_offering']
                user.cert_good_standing     = form.cleaned_data['cert_good_standing']
                user.status                 = 'Draft-id-comp'
                user.save()

                #<---------- Set session ---------->
                request.session['af_us'] = user.status

                messages.success(request, f'Data Company in USA has been submited.')
                return redirect('transactions:appointingfranchiseID')

        else:
            form = Franchise_Us_CompanyForm()

    if af_us:
        #<---------- Pocess Post with populated data ---------->
        populated_data = Transaction.objects.get(trans_id = af_trans_id)
        if request.method == 'POST':
            form = Franchise_Us_CompanyForm(request.POST, request.FILES, instance = populated_data)
            if form.is_valid():
                populated_data.comp_us_name           = form.cleaned_data['comp_us_name']
                populated_data.comp_us_president      = form.cleaned_data['comp_us_president']
                populated_data.comp_us_legal_status   = form.cleaned_data['comp_us_legal_status']
                populated_data.comp_us_establishment  = form.cleaned_data['comp_us_establishment']
                populated_data.comp_us_address        = form.cleaned_data['comp_us_address']
                populated_data.comp_us_state          = form.cleaned_data['comp_us_state']
                populated_data.comp_us_city           = form.cleaned_data['comp_us_city']
                populated_data.comp_us_zip            = form.cleaned_data['comp_us_zip']
                populated_data.comp_us_website        = form.cleaned_data['comp_us_website']
                populated_data.comp_us_phone          = form.cleaned_data['comp_us_phone']
                populated_data.comp_us_fax            = form.cleaned_data['comp_us_fax']
                populated_data.comp_us_email          = form.cleaned_data['comp_us_email']
                populated_data.line_of_business       = form.cleaned_data['line_of_business']
                populated_data.product_offering       = form.cleaned_data['product_offering']
                populated_data.cert_good_standing     = form.cleaned_data['cert_good_standing']
                populated_data.status                 = 'Draft-id-comp'
                populated_data.save()

                messages.success(request, f'Data Company in USA has been submited.')
                return redirect('transactions:appointingfranchiseID')

        else:
            form = Franchise_Us_CompanyForm(instance = populated_data)

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
        'form'              : form
    }

    return render(request,'transactions/trans-03-us-company-franchise.html', context)

@login_required
@user_passes_test(is_attache_staff)
def appointingfranchiseID(request):
    #<---------- Title ---------->
    title           = 'Franchise'
    form_title      = 'STATEMENT OF XA COMPANY DESIRING TO REGISTER A FRENCHISE BUSINESS IN XB'
    form_desc_title = 'This is to state that the following information is to appoint a representative, sales agent, or distributor in XB:'

    #<---------- Get session ---------->
    af_type     = request.session.get('af_type')
    af_trans_id = request.session.get('af_trans_id')
    af_us       = request.session.get('af_us')
    af_id       = request.session.get('af_id')

    #<---------- Check session ---------->
    if af_type == None and af_trans_id == None:
        return redirect('transactions:renewal_type_franchise')
    if af_us == None:
        return redirect('transactions:appointingfranchiseUS')
    if af_id == None:
        #<---------- Pocess Post ---------->
        user = Transaction.objects.get(trans_id = af_trans_id)
        if request.method == 'POST':
            form = Franchise_Id_CompanyForm(request.POST, request.FILES)
            if form.is_valid():
                user.comp_idn_name          = form.cleaned_data['comp_idn_name']
                user.comp_idn_president     = form.cleaned_data['comp_idn_president']
                user.comp_idn_address       = form.cleaned_data['comp_idn_address']
                user.comp_idn_province      = form.cleaned_data['comp_idn_province']
                user.comp_idn_city          = form.cleaned_data['comp_idn_city']
                user.comp_idn_zip           = form.cleaned_data['comp_idn_zip']
                user.comp_idn_website       = form.cleaned_data['comp_idn_website']
                user.comp_idn_phone         = form.cleaned_data['comp_idn_phone']
                user.comp_idn_fax           = form.cleaned_data['comp_idn_fax']
                user.comp_idn_email         = form.cleaned_data['comp_idn_email']
                user.term                   = form.cleaned_data['term']
                user.term_unit              = form.cleaned_data['term_unit']
                user.prospectus_agreement   = form.cleaned_data['prospectus_agreement']
                user.comp_idn_nationality   = form.cleaned_data['comp_idn_nationality']
                user.comp_idn_idnumber      = form.cleaned_data['comp_idn_idnumber']
                user.comp_idn_rep_officer   = form.cleaned_data['comp_idn_rep_officer']
                user.status                 = 'Draft-sign-comp'
                user.save()

                #<---------- Set session ---------->
                request.session['af_id'] = user.status

                messages.success(request, f'Data Company in Indonesia has been submited.')
                return redirect('transactions:appointingfranchiseApplicant')

        else:
            form = Franchise_Id_CompanyForm()

    if af_id:
        #<---------- Pocess Post with populated data ---------->
        populated_data = Transaction.objects.get(trans_id = af_trans_id)

        if request.method == 'POST':
            form = Franchise_Id_CompanyForm(request.POST, request.FILES, instance = populated_data)
            if form.is_valid():
                populated_data.comp_idn_name          = form.cleaned_data['comp_idn_name']
                populated_data.comp_idn_president     = form.cleaned_data['comp_idn_president']
                populated_data.comp_idn_address       = form.cleaned_data['comp_idn_address']
                populated_data.comp_idn_province      = form.cleaned_data['comp_idn_province']
                populated_data.comp_idn_city          = form.cleaned_data['comp_idn_city']
                populated_data.comp_idn_zip           = form.cleaned_data['comp_idn_zip']
                populated_data.comp_idn_website       = form.cleaned_data['comp_idn_website']
                populated_data.comp_idn_phone         = form.cleaned_data['comp_idn_phone']
                populated_data.comp_idn_fax           = form.cleaned_data['comp_idn_fax']
                populated_data.comp_idn_email         = form.cleaned_data['comp_idn_email']
                populated_data.term                   = form.cleaned_data['term']
                populated_data.term_unit              = form.cleaned_data['term_unit']
                populated_data.prospectus_agreement   = form.cleaned_data['prospectus_agreement']
                populated_data.comp_idn_nationality   = form.cleaned_data['comp_idn_nationality']
                populated_data.comp_idn_idnumber      = form.cleaned_data['comp_idn_idnumber']
                populated_data.comp_idn_rep_officer   = form.cleaned_data['comp_idn_rep_officer']
                populated_data.status                 = 'Draft-sign-comp'
                populated_data.save()

                messages.success(request, f'Data Company in Indonesia has been submited.')
                return redirect('transactions:appointingfranchiseApplicant')

        else:
            form = Franchise_Id_CompanyForm(instance = populated_data)

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
        'form'              : form
    }

    return render(request,'transactions/trans-04-id-company-franchise.html', context)

@login_required
@user_passes_test(is_attache_staff)
def appointingfranchiseApplicant(request):
    #<---------- Title ---------->
    title           = 'Franchise'
    form_title      = 'STATEMENT OF XA COMPANY DESIRING TO REGISTER A FRENCHISE BUSINESS IN XB'
    form_desc_title = 'This is to state that the following information is to appoint a representative, sales agent, or distributor in XB:'

    #<---------- Get session ---------->
    af_type     = request.session.get('af_type')
    af_trans_id = request.session.get('af_trans_id')
    af_us       = request.session.get('af_us')
    af_id       = request.session.get('af_id')
    af_app      = request.session.get('af_app')

    #<---------- Check session ---------->
    if af_type == None and af_trans_id == None:
        return redirect ('transactions:renewal_type_franchise')
    if af_us == None:
        return redirect ('transactions:appointingfranchiseUS')
    if af_id == None:
        return redirect ('transactions:appointingfranchiseID')
    if af_app == None:
        #<---------- Pocess Post ---------->
        user = Transaction.objects.get(trans_id = af_trans_id)
        if request.method == 'POST':
            form = ApplicantForm(request.POST, request.FILES)
            if form.is_valid():
                #<---------- Set Date ---------->
                datenow = timezone.now()

                #<---------- Save to table transaction ---------->
                user.applicant_name     = form.cleaned_data['applicant_name']
                user.applicant_position = form.cleaned_data['applicant_position']
                user.applicant_city     = form.cleaned_data['applicant_city']
                user.submit_date        = datenow
                user.status             = 'Submit'
                user.save()

                #<---------- Create Tracking ---------->
                track = MstTracking.objects.get(name = 'submitted')
                Trackings.objects.create(
                    trans_id    = user,
                    track_id    = track
                )

                #<---------- Create Logs ---------->
                Logs.objects.create(
                    trans_id    = user,
                    key         = 'status transaction',
                    old         = 'None',
                    new         = 'Submit',
                    user_id     = request.user.id,
                    timestamps  = datenow
                )

                #<---------- Delete transaction session ---------->
                del request.session['af_trans_id']
                del request.session['af_type']
                del request.session['af_us']
                del request.session['af_id']

                messages.success(request, f'All data has been submited, your registrtation is being processed.')
                return redirect('dashboards:dashboard')

        else:
            form = ApplicantForm()

    if af_app:
        #<---------- Pocess Post with populated data ---------->
        populated_data = Transaction.objects.get(trans_id = af_trans_id)
        if request.method == 'POST':
            form = ApplicantForm(request.POST, request.FILES, instance = populated_data)
            if form.is_valid():
                #<---------- Set Date ---------->
                datenow = timezone.now()

                #<---------- Save to table transaction ---------->
                populated_data.applicant_name     = form.cleaned_data['applicant_name']
                populated_data.applicant_position = form.cleaned_data['applicant_position']
                populated_data.applicant_city     = form.cleaned_data['applicant_city']
                populated_data.submit_date        = datenow
                populated_data.status             = 'Submit'
                populated_data.save()

                #<---------- Create Tracking ---------->
                track = MstTracking.objects.get(name = 'submitted')
                Trackings.objects.create(
                    trans_id    = populated_data,
                    track_id    = track
                )

                #<---------- Create Logs ---------->
                Logs.objects.create(
                    trans_id    = populated_data,
                    key         = 'status transaction',
                    old         = 'None',
                    new         = 'Submit',
                    user_id     = request.user.id,
                    timestamps  = datenow
                )

                #<---------- Delete transaction session ---------->
                del request.session['af_trans_id']
                del request.session['af_type']
                del request.session['af_us']
                del request.session['af_id']
                del request.session['af_app']
                del request.session['af_trans_cid']
                del request.session['af_trans_type']
                del request.session['af_trans_status']
                del request.session['af_checked']

                messages.success(request, f'All data has been submited, your registrtation is being processed.')
                return redirect('dashboards:dashboard')

        else:
            form = ApplicantForm(instance = populated_data)

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'form_title'        : form_title,
        'form_desc_title'   : form_desc_title,
        'form'              : form
    }

    return render(request,'transactions/trans-05-applicant.html', context)
''' <---------------------- End Appointing Franchise ----------------------> '''
