from django.shortcuts import render, redirect
from login_reg_app2.models import User
from quote_app.models import Quote
from django.contrib import messages
# Create your views here.
def view_all_quotes(request):
    if 'uid' in request.session:
        user = User.objects.filter(id=request.session['uid']).first()
        context = {
            'user': user,
            'quotes':  Quote.objects.all()
        }
        return render(request, 'all_quotes.html', context)
    return redirect('/')

def add_quote(request):
    if 'uid' in request.session:
        user = User.objects.filter(id=request.session['uid']).first()
        # validate quote
        errors = Quote.objects.validate_quote(request.POST)
        # if no errors create post
        if len(errors)==0:
            Quote.objects.create(
                owner = user,
                author = request.POST['author'],
                quote_text = request.POST['quote_text']
            )
        # if errors return the errors don't create quote
        else:
            for key, value in errors.items():
                messages.error(request, value)

        # always return to this page.
        return redirect('/quotes')

    return redirect('/')

def like_quote(request, quote_id):
    if 'uid' in request.session:
        user = User.objects.filter(id=request.session['uid']).first()
        print(quote_id,"_____________")
        #like the quote
        Quote.objects.filter(id=quote_id).first().liked_by.add(user)
        return redirect('/quotes')
    return redirect('/')

def view_user(request, user_id):
    if 'uid' in request.session:
        user_in_sesh = User.objects.filter(id=request.session['uid']).first()
        user = User.objects.filter(id=user_id).first()

        context ={
            'user': user,
            'quotes': Quote.objects.filter(owner=user),
            'user_in_sesh' : user_in_sesh,
        }

        return render(request, 'view_user.html', context)
    return redirect('/')

def delete_quote(request, quote_id):
    if 'uid' in request.session:
        user = User.objects.filter(id=request.session['uid']).first()
        quote = Quote.objects.filter(id=quote_id).first()

        if quote.owner == user:
            quote.delete()

        return redirect('/quotes')

    return redirect('/')