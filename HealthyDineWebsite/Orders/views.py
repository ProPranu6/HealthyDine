from django.shortcuts import render

from Review.models import Review

# Create your views here.
import json
from django.http import JsonResponse

from Food.models import Food
from .models import Order
from User.models import PreferredFood, PremiumUser, RegularUser

import re


def extract_and_dump_food_interests(request):
    print("extracting old food interests and dumping new food interests ... ")
    usrids = set([orde.usr_id for orde in Order.objects.all()]) 
    for usr_id in usrids:
        usr_food_interests = []
        already_collected = []
        for orde in Order.objects.all():
            if orde.food_id not in already_collected:
                usr_food_interests += orde.extract_food_interests(usr_id)
                already_collected.append(orde.food_id)
        
        PreferredFood.objects.filter(user=usr_id).delete()
        
        for rec in usr_food_interests:
            PreferredFood.objects.create(user=rec[0], pfood=rec[1])
    return JsonResponse(1, safe=False) 
    

def food_for_display(cart):
    food_info = []
    fd_objects = []
    for fd in cart.keys():
        fd_objects.append(Food.objects.raw("select * from food_food where id = %s", [int(fd)])[0])
    fd_objects = [(fo.food_name, fo.carbs, fo.proteins, fo.fats, fo.key_ingredient1, fo.key_ingredient2, fo.key_ingredient3, fo.key_ingredient4, fo.key_ingredient5, fo.image_path, fo.id, int(cart[str(fo.id)])) for fo in fd_objects]
    
    for vv in fd_objects:
        short_path = '/Images/'+ re.findall('[A-Z]_[0-9]{2}.jpg', vv[9])[0]
        food_info.append({'name' : vv[0], 'carbs':vv[1], 'proteins':vv[2], 'fats':vv[3], 'keying1':vv[4], 'keying2' : vv[5], 'keying3':vv[6], 'keying4':vv[7], 'keying5':vv[8], 'image':short_path, 'id':vv[10], 'quant':vv[11]})
    
    return food_info

def food_for_review(for_user):
    
    orders_to_consider = set(Order.objects.filter(usr_id=for_user).order_by('-id')[:3]) #last 3 orders by the particular user
    fd_objects = []
    for fd in orders_to_consider:
        fo = Food.objects.raw("select * from food_food where id = %s", [fd.food_id])[0]
        fd_objects.append((fo.food_name, fo.carbs, fo.proteins, fo.fats, fo.key_ingredient1, fo.key_ingredient2, fo.key_ingredient3, fo.key_ingredient4, fo.key_ingredient5, fo.image_path, fo.id))
    
    food_review_info = []
    for vv in fd_objects:
        short_path = '/Images/'+ re.findall('[A-Z]_[0-9]{2}.jpg', vv[9])[0]
        food_review_info.append({'name' : vv[0], 'carbs':vv[1], 'proteins':vv[2], 'fats':vv[3], 'keying1':vv[4], 'keying2' : vv[5], 'keying3':vv[6], 'keying4':vv[7], 'keying5':vv[8], 'image':short_path, 'id':vv[10]})
    
    return food_review_info
    
def order_list(request):
   
    if request.method == "POST":
        
        revs = json.loads(request.body.decode("utf-8"))
        print(revs)
        for food_id, rev in revs.items():
            if food_id.isdigit():
                if rev.isdigit():
                    Review.objects.create(rev_type="discrete", rev_rating=int(rev), food_id=int(food_id))
                    print("Review considered ... ")
                elif rev != "":
                    Review.objects.create(rev_type="descriptive", rev_content=rev, food_id=int(food_id))
                    print("Review considered ... ")
                else:
                    pass
        print("Redirecting to Payment Page ...")
        return render(request, 'intro.html')
        
    
    food_info = food_for_display(request.session['cart'])
    food_review_info = food_for_review(request.session['user'])
    
    
    return render(request, 'orders.html', {'food_info':food_info, 'food_review_info':food_review_info})


def add_to_cart(request):
    CART = request.session['cart']
    res = json.loads(request.body.decode("utf-8"))
    
    
    if res['food_id'] != "":
        if res['food_id'] not in CART:
            if int(res['actual_freq']) == -1:
                CART[res['food_id']] = 1
            else:
                CART[res['food_id']] = int(res['actual_freq'])

        else:
            if int(res['actual_freq']) == -1:
                CART[res['food_id']] += 1
            else:
                CART[res['food_id']] = int(res['actual_freq'])

    print("Present cart " ,CART)
    request.session['cart'] = CART
    return JsonResponse(CART, safe=False)

def delete_from_cart(request):
    res = json.loads(request.body.decode("utf-8"))
    CART = request.session['cart']
    if res['food_id'] not in CART or (res['food_id'] == 0):
        print(f"No Item of : {res['food_id']} to remove")
        #CART[res['food_id']] = 1
    else:
        CART[res['food_id']] = max(0, CART[res['food_id']]-res['quant'])
    print(CART)
    request.session['cart'] = CART
    return JsonResponse(CART, safe=False)
    
def confirm_cart(request):   #triggered when checkout is pressed on orders page
    res = json.loads(request.body.decode("utf-8"))
    request.session['cart_value'] = round(res['cart_total'], 2)
    CART = request.session['cart']
    if request.session['user_type'] != "prem":
        print("Sucessfully dumped cart empty ...")
        return JsonResponse(request.session['cart'])
        
    for food_id, quant in CART.items():
        Order.objects.create(usr_id=request.session['user'], food_id=int(food_id), quant=quant)
    
    print("Successfully added cart to orders ...")
    return JsonResponse(request.session['cart'])
        
    
def payment(request):
    if 'from_signup' in request.session:
        form = request.session['from_signup']
        user_id = form['user_id']
        password = form['password'] #models.CharField(max_length=30)
        mail_id = form['mail_id']  #models.CharField(max_length=30)
        contact_no = form['contact_no'] #models.IntegerField()
        location = form['location']#models.CharField(max_length=30)
        height = form['height']
        weight = form['weight']
        cal_intake = form['calories_intake']
        puser = PremiumUser(user_id=user_id,password=password,mail_id=mail_id, contact_no=contact_no, location=location, height=height, weight=weight,calories_intake=cal_intake)
        puser.save()
            
            #dump_interests()
        
        user_info = {'name' : user_id, 'mail':mail_id, 'mobile' :contact_no, 'location':location}
        
    else:
        user_info = {'name' : request.session['user_name'], 'mail':request.session['user_email'], 'mobile' :request.session['user_contact'], 'location':request.session['user_location']}
        
    return render(request, 'Checkout.html', {'user_info':user_info})  #payment page comes here

def success_page(request):
    if 'from_signup' in request.session:
        bill = 25 #premium user amount
        bill_type = 'subscription'
        del request.session['from_signup']
    else:
        bill = request.session['cart_value']
        bill_type = 'orders'
        
    request.session['cart_value'] = 0
    request.session['cart'] = dict()
    return render(request, 'successpage.html', {'bill': bill, 'bill_type':bill_type})
       