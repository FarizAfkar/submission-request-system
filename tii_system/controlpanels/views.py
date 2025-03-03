from datetime import datetime
from io import BytesIO
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction, TransactionTypes, Documents , Logs , MstTracking , Trackings
from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger
from controlpanels.renders import Render
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, message
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files import File

# Create your views here.
''' <------------------------ Check Attache Staff -------------------------> '''
def is_attache_staff(user):
    if user.groups.filter(name = 'attache staff').exists():
        return True
    else:
        raise PermissionDenied()
''' <---------------------- End  Check Attache Staff ----------------------> '''


''' <------------------------- Send Email and PDF -------------------------> '''
def send_email_transaction(params_pdf:dict, params_email:dict):
    status = ''
    try :
        #<---------- Reference Params ---------->

        # params_pdf = {
        #     'trans'           : trans,
        #     'trans_subject_1' : trans_subject_1,
        #     'trans_subject_2' : trans_subject_2,
        #     'trans_detail'    : trans_detail,
        #     'trans_activity_1': trans_activity_1,
        #     'trans_activity_2': trans_activity_2,
        # }

        # params_email = {
        #     'cc'          : cc,
        #     'bcc'         : bcc,
        #     'to'          : to,
        #     'subject'     : subject,
        #     'applicant'   : applicant,
        #     'trans_type'  : trans_type,
        # }

        #<---------- Create PDF ---------->
        files_letter        = Render.render('controlpanels/pdf-letter.html', params_pdf)
        files_registration  = Render.render('controlpanels/pdf-registration.html', params_pdf)

        #<---------- Set File Name ---------->
        file_name_letter        = '{0}-{1}-{2}.pdf'.format('Letter',
                                    params_pdf['trans'].trans_type_id.description,
                                    params_pdf['trans'].registration_code)
        file_name_registration  = '{0}-{1}-{2}.pdf'.format('Registration',
                                    params_pdf['trans'].trans_type_id.description,
                                    params_pdf['trans'].registration_code)

        #<---------- Set Email ---------->
        cc      = params_email['cc']
        bcc     = params_email['bcc']
        to      = params_email['to']
        subject = params_email['subject']
        message = render_to_string('controlpanels/email-transactions.html', params_email)

        #<---------- Send Email ---------->
        mail = EmailMultiAlternatives(subject, message, to = [to], cc = [cc], bcc = [bcc])
        mail.attach(file_name_letter, files_letter.getvalue(), 'application/pdf')
        mail.attach(file_name_registration, files_registration.getvalue(), 'application/pdf')
        mail.content_subtype = 'html'
        mail.send(fail_silently = False)

        #<---------- Save PDF Letter to Documents ---------->
        doc_letter = Documents.objects.create(
            date_generated  = timezone.now(),
            trans_id        = params_pdf['trans']
        )
        doc_letter.file_location.save(file_name_letter, File(BytesIO(files_letter.content)))

        #<---------- Save PDF Registration to Documents ---------->
        doc_registration = Documents.objects.create(
            date_generated  = timezone.now(),
            trans_id        = params_pdf['trans']
        )
        doc_registration.file_location.save(file_name_registration, File(BytesIO(files_registration.content)))

        #<---------- Set Success Return ---------->
        status = {'200':'ok'}

    except Exception as e:
        #<---------- Set Error Return ---------->
        print('this is error', e)
        status = {'400': '{}'.format(e)}

    return status
''' <----------------------- End Send Email and PDF -----------------------> '''

''' <------------------------- Send Email and PDF -------------------------> '''
def send_email_rejection(params_email:dict):
    status = ''
    try :
        #<---------- Reference Params ---------->

        # params_email = {
        #     'cc'          : cc,
        #     'bcc'         : bcc,
        #     'to'          : to,
        #     'subject'     : subject,
        #     'applicant'   : applicant,
        #     'trans_type'  : trans_type,
        #     'notes'       : rejection_note,
        # }

        #<---------- Set Email ---------->
        cc      = params_email['cc']
        bcc     = params_email['bcc']
        to      = params_email['to']
        subject = params_email['subject']
        message = render_to_string('controlpanels/email-rejection.html', params_email)

        #<---------- Send Email ---------->
        mail = EmailMultiAlternatives(subject, message, to = [to], cc = [cc], bcc = [bcc])
        mail.content_subtype = 'html'
        mail.send(fail_silently = False)

        #<---------- Set Success Return ---------->
        status = {'200':'ok'}

    except Exception as e:
        #<---------- Set Error Return ---------->
        print('this is error', e)
        status = {'400': '{}'.format(e)}

    return status
''' <----------------------- End Send Email and PDF -----------------------> '''


''' <-------------------------- Transaction List --------------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def cpanel_list(request):
    #<---------- Get List Transaction ---------->
    TRANS_STATUS = ['Submit', 'Decline', 'Verified', 'Approve', 'Preparing Document', 'Complete']
    trans = Transaction.objects.filter(status__in = TRANS_STATUS).order_by('submit_date')

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

    return render(request, 'controlpanels/cpanel-list.html' , context)
''' <------------------------ End Transaction List ------------------------> '''


''' <------------------------ Transaction Approval ------------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def cpanel_approval(request , registration_code):
    #<---------- Get Transaction ---------->
    trans = Transaction.objects.get(registration_code = registration_code)

    #<---------- Check Status ---------->
    TRANS_STATUS = ['Submit', 'Decline', 'Verified', 'Approve', 'Complete']
    if trans.status not in TRANS_STATUS:
        raise PermissionDenied()

    #<---------- Create Tracking  ---------->
    track = MstTracking.objects.get(name = 'processing')

    #<---------- Check IF Transaction in Process ---------->
    check_track = Trackings.objects.filter(trans_id = trans, track_id = track)
    if check_track.count() == 0:
        Trackings.objects.create(
            trans_id    = trans,
            track_id    = track
        )

    #<---------- Revise Process ---------->
    revise = False
    if Trackings.objects.filter(trans_id = trans, track_id__name = 'revise').exists():
        revise = True

    #<---------- Pocess Post ---------->
    if request.method == 'POST':

        #<---------- Verify ---------->
        if request.POST.get('Verify'):
            #<---------- Set Date ---------->
            datenow = timezone.now()

            #<---------- Update Status transaction ---------->
            trans.approval_id   = request.user.id # auth_user_id
            trans.approval_name = f'{request.user.first_name} {request.user.last_name}'
            trans.approval_date = datenow
            trans.status        = 'Verified'
            trans.save()

            #<---------- Create Tracking ---------->
            track = MstTracking.objects.get(name = 'wait approval')
            Trackings.objects.create(
                trans_id    = trans,
                track_id    = track
            )

            #<---------- Update Logs ---------->
            update_logs             = Logs.objects.get(trans_id = trans)
            update_logs.key         = 'status transaction'
            update_logs.old         = 'Submit'
            update_logs.new         = 'Verified'
            update_logs.user_id     = int(request.user.id)
            update_logs.timestamps  = datenow
            update_logs.save()

            messages.info(request, f'Registration with ID {registration_code} has been Verified.')

        #<---------- Approve ---------->
        if request.POST.get('Approve'):
            #<---------- Set Date ---------->
            datenow = timezone.now()

            #<---------- Update Status transaction ---------->
            trans.approval_id   = request.user.id # auth_user_id
            trans.approval_name = f'{request.user.first_name} {request.user.last_name}'
            trans.approval_date = datenow
            trans.status        = 'Approve'
            trans.save()

            #<---------- Create Tracking ---------->
            track = MstTracking.objects.get(name = 'approved')
            Trackings.objects.create(
                trans_id    = trans,
                track_id    = track
            )

            #<---------- Update Logs ---------->
            update_logs             = Logs.objects.get(trans_id = trans)
            update_logs.key         = 'status transaction'
            update_logs.old         = 'Verified'
            update_logs.new         = 'Approve'
            update_logs.user_id     = int(request.user.id)
            update_logs.timestamps  = datenow
            update_logs.save()

            messages.info(request, f'Registration with ID {registration_code} has been Approved.')

            #<---------- Send Email and Attachment ---------->
            try:
                #<---------- Update Status transaction ---------->
                trans.status = 'Preparing Document'
                trans.save()

                #<---------- Update Logs ---------->
                update_logs             = Logs.objects.get(trans_id = trans)
                update_logs.key         = 'status transaction'
                update_logs.old         = 'Approve'
                update_logs.new         = 'Preparing Document'
                update_logs.user_id     = int(request.user.id)
                update_logs.timestamps  = datenow
                update_logs.save()

                #<---------- Get Data Related ---------->
                applicant       = User.objects.get(username = trans.cid)
                cc              = ''
                bcc             = ''
                to              = trans.comp_us_email
                renewal         = trans.renewal_type.capitalize()
                trans_type      = trans.trans_type_id.description
                applicant_name  = f'{applicant.first_name} {applicant.last_name}'

                #<---------- Set Params PDF ---------->
                params_pdf = {
                    'trans'           : trans,
                    'trans_subject_1' : f'{renewal} {trans_type}',
                    'trans_subject_2' : '',
                    'trans_detail'    : {trans_type},
                    'trans_activity_1': '',
                    'trans_activity_2': '',
                }

                #<---------- Set Params Email ---------->
                params_email = {
                    'cc'          : cc,
                    'bcc'         : bcc,
                    'to'          : to,
                    'subject'     : f'{renewal} Registation {trans_type}',
                    'applicant'   : applicant_name,
                    'trans_type'  : trans_type,
                }

                #<---------- Send Email Function ---------->
                send_request = send_email_transaction(params_pdf, params_email)

                #<---------- Check Response Data ---------->
                if '200' in send_request.keys():
                    #<---------- Update Status transaction ---------->
                    trans.status = 'Complete'
                    trans.save()

                    #<---------- Update Logs ---------->
                    update_logs             = Logs.objects.get(trans_id = trans)
                    update_logs.key         = 'status transaction'
                    update_logs.old         = 'Preparing Document'
                    update_logs.new         = 'Complete'
                    update_logs.user_id     = int(request.user.id)
                    update_logs.timestamps  = datenow
                    update_logs.save()

                    messages.success(request, f'Email with Attachment has been send. Process registration completed')

                    #<---------- Create Tracking ---------->
                    track = MstTracking.objects.get(name = 'complete')
                    Trackings.objects.create(
                        trans_id    = trans,
                        track_id    = track
                    )

                elif '400' in send_request.keys():
                    messages.error(request, f'Whoops Something Wrong... {send_request.values()}')

            except Exception as e:
                messages.error(request, f'Whoops Something Wrong... {e}')

    #<---------- Render Html Context ---------->
    context = {
        'trans' : trans,
        'revise': revise
    }

    return render(request, 'controlpanels/cpanel-approval.html' , context)
''' <---------------------- End Transaction Approval ----------------------> '''


''' <---------------------- Transaction Form Reject -----------------------> '''
@login_required
@user_passes_test(is_attache_staff)
def cpanel_reject(request , registration_code):
    #<---------- Get Transaction --------------->
    trans = Transaction.objects.get(registration_code = registration_code)

    #<---------- Check Status ---------->
    TRANS_STATUS = ['Submit', 'Verified']
    if trans.status not in TRANS_STATUS:
        raise PermissionDenied()

    #<---------- Pocess Post ---------->
    if request.method == 'POST':
        #<---------- Set Date ---------->
        datenow = timezone.now()

        #<---------- Get Note ---------->
        rejection_note = request.POST.get('rejection-note')

        #<---------- Reject ---------->
        if request.POST.get('Reject'):

            #<---------- Update Logs ---------->
            update_logs             = Logs.objects.get(trans_id = trans)
            update_logs.key         = 'status transaction'
            update_logs.old         = trans.status
            update_logs.new         = 'Decline'
            update_logs.user_id     = int(request.user.id)
            update_logs.timestamps  = datenow
            update_logs.save()

            #<---------- Update Status transaction ---------->
            trans.approval_id   = request.user.id # auth_user_id
            trans.approval_name = f'{request.user.first_name} {request.user.last_name}'
            trans.approval_date = datenow
            trans.notes         = rejection_note
            trans.status        = 'Decline'
            trans.save()

            #<---------- Create Tracking ---------->
            track = MstTracking.objects.get(name = 'rejected')
            Trackings.objects.create(
                trans_id    = trans,
                track_id    = track
            )

            #<---------- Send Email Rejection  ---------->
            try:

                #<---------- Get Data Related ---------->
                applicant       = User.objects.get(username = trans.cid)
                cc              = ''
                bcc             = ''
                to              = trans.comp_us_email
                subject         = 'Rejection'
                trans_type      = trans.trans_type_id.description
                applicant_name  = f'{applicant.first_name} {applicant.last_name}'

                # <------------------ Set Params Email ---------->
                params_email = {
                    'cc'          : cc,
                    'bcc'         : bcc,
                    'to'          : to,
                    'subject'     : f'{subject} Registation {trans_type}',
                    'applicant'   : applicant_name,
                    'trans_type'  : trans_type,
                    'notes'       : rejection_note
                }

                #<---------- Send Email Function ---------->
                send_request = send_email_rejection(params_email)

                #<---------- Check Response Data ---------->
                if '200' in send_request.keys():
                    messages.success(request, f'Email has been send. Process rejection completed')

                elif '400' in send_request.keys():
                    messages.error(request, f'Whoops Something Wrong... {send_request.values()}')

            except Exception as e:
                messages.error(request, f'Whoops Something Wrong... {e}')

            messages.info(request, f'Registration with ID {registration_code} has been Rejected.')

        return redirect('c-panels:list-transaction')

    #<---------- Render Html Context ---------->
    context = {
        'trans' : trans
    }

    return render(request, 'controlpanels/cpanel-reject.html' , context)
''' <-------------------- END Transaction Form Reject ---------------------> '''
