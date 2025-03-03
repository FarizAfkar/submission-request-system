"""Module providing a function printing python version."""
from django.shortcuts import render
from transactions.models import Transaction , Trackings

# Create your views here.
def home(request):
    """Module providing a function printing python version."""
    #<---------- Title ---------->
    title   = 'Home'

    #<---------- Render Html Context ---------->
    context = {'title' : title}

    return render(request, 'portalpages/home.html', context)

def representative(request):
    """Module providing a function printing python version."""
    #<---------- Title ---------->
    title   = 'Representative Office'

    #<---------- Render Html Context ---------->
    context = {'title' : title}

    return render(request, 'portalpages/representative.html', context)

def agentdistributor(request):
    """Module providing a function printing python version."""
    #<---------- Title ---------->
    title   = 'Agent/Distributor'

    #<---------- Render Html Context ---------->
    context = {'title' : title}

    return render(request, 'portalpages/agentdistributor.html', context)

def franchise(request):
    """Module providing a function printing python version."""
    #<---------- Title ---------->
    title   = 'Franchise'

    #<---------- Render Html Context ---------->
    context = {'title' : title}

    return render(request, 'portalpages/franchise.html', context)

def tracking(request):
    """Module providing a function printing python version."""
    #<---------- Title ---------->
    title = 'Transaction Tracking System'

    #<---------- Set Variable ---------->
    error_flag        = False
    error_message     = ''
    registration_code = ''
    transaction       = ''
    track             = ''

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
                    trans_status = ['Draft-us-comp', 'Draft-id-comp', 'Draft-sign-comp']
                    if transaction.status in trans_status:
                        error_message = 'Sorry, The registration code that you entered is incorrect or invalid. \
                                        please try again and remember The Registration Code are Case Sensitive.'

                    # Check Tracking
                    track    = Trackings.objects.filter(trans_id = transaction).order_by('timestamps')
                    if track.count() == 0:
                        error_message = 'Sorry, The registration code that you entered is incorrect or invalid. \
                                        please try again and remember The Registration Code are Case Sensitive.'
                else:
                    error_message = 'Sorry, The registration code that you entered is incorrect or invalid.\
                                    please try again and remember The Registration Code are Case Sensitive.'
        else:
            error_flag = True

    #<---------- Render Html Context ---------->
    context = {
        'title'             : title,
        'transaction'       : transaction,
        'tracking'          : track,
        'error_flag'        : error_flag,
        'error_message'     : error_message,
        'registration_code' : registration_code
    }

    return render(request, 'portalpages/tracking.html', context)

def homepage_help(request):
    """Module providing a function printing python version."""
    #<---------- Title ---------->
    title   = 'Help'

    #<---------- Render Html Context ---------->
    context = {'title' : title}

    return render(request, 'portalpages/help.html', context)
