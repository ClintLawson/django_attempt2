from django.shortcuts import render, HttpResponse, redirect
from login_reg_app2.models import User
from django.contrib import messages

# Create your views here.
def view_login_register(request):
    return render(request, "login_register.html")

def register(request):
    # validate registration attempt
    errors = User.objects.registration_validation(request.POST)
    
    # if there are errors return error messages
    if len(errors)>0:
        #dump errors into messages for html page
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    # otherwise register user and log them in!    
    else:
        # register user in db and get ID
        user_id = User.objects.register_user(request.POST)
        # log user into session
        request.session['uid'] = user_id
        print('registered___________')
        return redirect('/quotes') #________________________change this out for new projects

def login(request):
    attempt = User.objects.login_validation(request.POST)
    if attempt == True:
        request.session['uid'] = User.objects.filter(email=request.POST['email'])[0].id
        print('logged in__________')
        return redirect('/quotes') #_________________________change this out for new projects
    else:
        messages.error(request, attempt)
        return redirect('/')

def logout(request):
    request.session.flush() 
    return redirect('/')

def edit_account(request):
    # check to make sure user is in session!!!
    if 'uid' in request.session:
        user = User.objects.get(id=request.session['uid'])
        context = {
            'user': user
        }
        return render(request, "edit_account.html", context) 

    else:
        return redirect('/')

def update_account(request):
    # check to make sure user is in session!!!
    if 'uid' in request.session:
        user = User.objects.filter(id=request.session['uid']).first()
        print(request.POST,"_____________")

        errors = User.objects.update_user(request.POST, user)
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/edit_account')  

    else:
        return redirect('/')