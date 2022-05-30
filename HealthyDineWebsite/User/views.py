from django.shortcuts import render, redirect
from .forms import SignupFormReg, SignupFormPrem, LoginForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import RegularUser, PremiumUser, PreferredFood, AllergyFood
from Food.models import Food


import json
import requests

import re
import random 

DUMP_INTERESTS = 0
DELETE_INOW = 0

DUMP_ALLERGIES = 0
DELETE_ANOW = 0

def dump_interests():
    print("dumping interest ... ")
    all_foods = Food.objects.all()
    for usr in PremiumUser.objects.all():
        interests = set()
        for i in range(20):
            pfd = random.choice(all_foods)
            interests.add(pfd)
        for fd in interests:
            PreferredFood.objects.create(user=usr, pfood=fd)
    return

def dump_allergies():
    print("dumping allergies ... ")
    all_foods = Food.objects.all()
    for usr in PremiumUser.objects.all():
        allergies = set()
        for i in range(3):
            pfd = random.choice(all_foods)
            allergies.add(pfd.key_ingredient3)
        for fd in allergies:
            AllergyFood.objects.create(user=usr, afood=fd)
    return
    
if DUMP_INTERESTS:
    dump_interests()
if DELETE_INOW:
    print("deleting interests ...")
    PreferredFood.objects.all().delete()
    
if DUMP_ALLERGIES:
    dump_allergies()
if DELETE_ANOW:
    print("deleting allergies ...")
    AllergyFood.objects.all().delete()
        
         
def intro(request):
    return render(request, 'intropage1.html')
def signup_regular(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        
        form = SignupFormReg(request.POST)
    
        if form.is_valid():
            
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password'] 
            mail_id = form.cleaned_data['mail_id']  
            contact_no = form.cleaned_data['contact_no'] 
            location = form.cleaned_data['location']
            
            ruser = RegularUser(user_id=user_id,password=password,mail_id=mail_id, contact_no=contact_no, location=location)
            ruser.save()
            return render(request, 'thank_you.html', {'user_name':user_id})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupFormReg()
        SESSION_USER = None
        SESSION_USER_DATA = None

    return render(request, 'signup_reg.html', {'form': form})

def signup_premium(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupFormPrem(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            
            
            # redirect to a new URL:
           
            request.session['from_signup'] = form.cleaned_data
            
            return redirect(reverse('payments')) # # render(request, 'thank_you.html', {'user_name':user_id})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupFormPrem()
        try:
            del request.session['user']
        except:
            pass
        try:
            del request.session['user_data']
        except:
            pass

    return render(request, 'signup_prem.html', {'form': form})


def shorten_filts(filts):
    tfilts = {}
    for k, v in filts.items() : 
        if len(v) != 0:
            li = []

            for vv in v:
                short_path = '/Images/'+ re.findall('[A-Z]_[0-9]{2}.jpg', vv[9])[0]
                li.append({'name' :vv[0], 'image' :short_path, 'id':vv[11]})
            tfilts[k] = li  
        else:
            tfilts[k] = []
    return tfilts



def login(request):
    
    if request.session.get('user') != None:
        return render(request, 'usrhome.html', {'filts':request.session['user_data']})      
    request.session['cart'] = dict()
    
    if request.method == 'POST':
        
        form = LoginForm(request.POST)
        
        if form.is_valid():
           
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password'] 
            
            resp = RegularUser.objects.raw('select * from user_regularuser where user_id = %s and password = %s', [user_id, password])
           
            if len(resp) != 0:
                
                resp = resp[0]
                act_type = "reg"
                if resp.password == password:
                    
                    request.session['user'] = resp.id
                    request.session['user_type'] = act_type
                    request.session['user_name'] = resp.user_id
                    request.session['user_email'] = resp.mail_id
                    request.session['user_contact'] = resp.contact_no
                    request.session['user_location'] = resp.location
                    
                    res = requests.post('http://127.0.0.1:8000/food/homepage/', data={"resp" :resp, "act_type":act_type})
                    try:
                        filts = json.loads(res.content.decode("utf-8"))
                        
                        #carbs : [name, carbs, proteins, fats, keyingredients1-5, image_path, item_rating]
                        #tcarbs : [name, image_path]
                        sfilts = shorten_filts(filts)
                       
                    except Exception as e:
                        print("Exception in login for regular user : ", e)
                        pass
                    
                    request.session['user_data'] = sfilts
                    return render(request, 'usrhome.html', {'filts':sfilts})         
                else:
                    return render(request, 'login_error.html', {'user_type':"Regular"})
            else:
                
                act_type="prem"
                resp = PremiumUser.objects.raw('select * from user_premiumuser where user_id = %s and password = %s', [user_id, password])
                
                if len(resp) != 0:
                    resp = resp[0]
                    
                    request.session['user'] = resp.id
                    request.session['user_type'] = act_type
                    request.session['user_name'] = resp.user_id
                    request.session['user_email'] = resp.mail_id
                    request.session['user_contact'] = resp.contact_no
                    request.session['user_location'] = resp.location
                    
                    res = requests.post('http://127.0.0.1:8000/food/homepage/', data={"id":resp.id, "height" :resp.height,"weight":resp.weight, "act_type":act_type, "user_name":request.session['user_name'], "cal_intake":resp.calories_intake})
                    
                    try:
                        filts = json.loads(res.content.decode("utf-8"))
                        #carbs : [name, carbs, proteins, fats, keyingredients1-5, image_path, item_rating]
                        #tcarbs : [name, image_path]
                        sfilts = shorten_filts(filts)
                        
                    except:
                        sfilts = {'carbs':[], 'proteins':[], 'fats':[]}
                    
                    request.session['user_data'] = sfilts
                    return render(request, 'usrhome.html', {'filts':sfilts})
                else:
                    return render(request, 'login_error.html', {'user_type':"Premium"})
            
            

    # if a GET (or any other method) we'll create a blank form
    else:
        
        form = LoginForm()
        try:
            del request.session['user']
        except:
            pass
        try:
            del request.session['user_data']
        except:
            pass

        return render(request, 'login.html', {'form': form})
    

def logout(request):
    try:
        del request.session['user']
    except:
        pass
    try:
        del request.session['user_data']
    except:
        pass
    
    form = LoginForm()
    return render(request, 'login.html', {'form': form})
    
    

    
    





