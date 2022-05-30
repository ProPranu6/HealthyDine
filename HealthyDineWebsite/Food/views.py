from django.shortcuts import render

# Create your views here.
from .models import Food
from requests import Response
import requests
import json
import re
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse

from User.models import PreferredFood, AllergyFood
from datetime import datetime, timedelta
from Orders.models import Order

DUMP_NOW = 0
DELETE_NOW = 0

def dump_food():
    print("Dumping food now ...")
    with open(r'C:\Users\T.PRANEETH\Desktop\Semester 6\Software Engineering\HealthyDine\djangostuff\DJhealthydine\Food\FoodDumpData\data_SE.txt') as f:
        data = eval(f.read())
    for rec in data:
        food_instance = Food.objects.create(food_name=rec[1], carbs=rec[2], proteins=rec[3], fats=rec[4], key_ingredient1=rec[5], key_ingredient2=rec[6], key_ingredient3=rec[7], key_ingredient4=rec[8], key_ingredient5=rec[9], image_path = r'C:\Users\T.PRANEETH\Desktop\Semester 6\Software Engineering\HealthyDine\djangostuff\DJhealthydine\Food\FoodDumpData\Images'+str(rec[10]), item_rating=0.0)
    return

if DUMP_NOW:
    dump_food()
if DELETE_NOW:
    Food.objects.all().delete()

class FoodRecommender:
    def __init__(self, *args):
        self.filts = [f for f in args]
    def __call__(self, X):
        try:
            for fil in self.filts:
                X = fil(X)
            return X
        except :
            print("Please include necessary filters in the pipeline")
        
from transformers import pipeline
                
class ReviewHandler:
    sentiment_analysis = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english")
    reviewer = sentiment_analysis
    
    @classmethod
    def generate_overall_rating(cls, rev_types, revs):
        overall_rating = 0
        for rev_type, rev in zip(rev_types, revs):
            if rev_type == 'descr':
                result = cls.reviewer(rev)[0]
                overall_rating += result['score'] if result['label'] == 'POSITIVE' else 1-result['score']
            else:
                overall_rating += (rev - 1)/(4)
        return overall_rating/len(rev_types)
    
    @classmethod
    def set_overall_rating(cls, reviews):
        ##connect to database and set the overall rating of restaurants, delivery_personnel and items
        
        items = list(set([rev.item_id for rev in reviews]))
        
        for it in items:
            rev_types = []
            revs = []
            for rev in reviews:
                if it == rev.item_id:
                    rev_types += [rev.rev_type]
                    revs += [rev.rev]
            overall_rating = cls.generate_overall_rating(rev_types, revs)
            print(f"{it} => {overall_rating}")
        return
    
    @classmethod
    def generate_items_rated_list(cls, item_list):
        rated_list = sorted(item_list, key=lambda x: x.rating, reverse=True)
        return rated_list

class util:
    def __init__(self):
        pass
    def len_(self, obj):
        c = 0
        for v in obj.values():
            c += len(v)
        return c
    def disp_(self, obj):
        if type(obj) == type([]):
            print("Foods:")
            for c in obj:
                print("\t",c.name)
        else:
            for c in obj.keys():
                print(c,":")
                for v in obj[c]:
                    print("\t",v.name)
                    
from math import ceil
from tensorflow import keras
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
import numpy as np
import copy

class BMIFilter:
    def __init__(self, height, weight, calories_intake, strict_diet=True):
        self.height = height
        self.weight = weight
        self.calories_intake=calories_intake
        self.strict_diet=strict_diet
        self.Ddays = 0
        self.share = None
        
        
    def __getIdealWeight(self):
        return 22*self.height**2
    
    def __getRevisedCaloriesPerDay(self, weight_gap, per_day_cal=2500, strict=True):  #Per day calories intake calculated from the user data during data gathering period
        max_revised_cals = per_day_cal - 500       #A minimum of 500 calories per day has to be burnt
        if strict:
            diet_days = 1
            rc = per_day_cal - weight_gap*7700/diet_days
            while rc<500:                         #Minimum of 500 calories per day has to be consumed
                diet_days += 1
                rc = per_day_cal - weight_gap*7700/diet_days 
            return diet_days, rc
        else:
            return 7700*weight_gap/500, max_revised_cals 


    def __getCaloriesSplit(self, total_calories):
        carbs_split = 0.45
        proteins_split = 0.35
        fats_split = 0.2
        return {'carbs' : carbs_split*total_calories, 'proteins':proteins_split*total_calories, 'fats':fats_split*total_calories}
    
    def __set_predominance(self, food_items):
        for fi in food_items:
            total_cal = fi.carbs + fi.proteins + fi.fats
            relative_fraction_carbs, relative_fraction_proteins, relative_fraction_fats = (fi.carbs/total_cal)/0.45, (fi.proteins/total_cal)/0.35 , (fi.fats/total_cal)/0.2  
            if  relative_fraction_carbs > relative_fraction_proteins and relative_fraction_carbs > relative_fraction_fats:
                fi.predominance = 'carbs'
            elif relative_fraction_proteins > relative_fraction_carbs and relative_fraction_proteins > relative_fraction_fats: 
                fi.predominance = 'proteins'
            else:
                fi.predominance = 'carbohydrates'
            #print(fi, fi.predominance)

        return food_items
        
    def __call__(self, food_items, topn=3):
        food_items = copy.deepcopy(food_items)
        food_items = self.__set_predominance(food_items)
        wi = self.__getIdealWeight()
        D, rc = self.__getRevisedCaloriesPerDay(self.weight-wi,self.calories_intake,self.strict_diet)
        self.Ddays = ceil(D)
        share = self.__getCaloriesSplit(rc)
        self.share = share
        filtered_list = {'carbs':[], 'proteins':[], 'fats':[]}
        for mn in filtered_list.keys():
            food_cons = [ fi for fi in sorted(food_items, key=lambda x: eval(f'x.{mn}'), reverse=True) if eval(f'fi.{mn}')<= share[mn] and (fi.predominance == mn or 1)][:topn]
            filtered_list[mn] = food_cons
            for i in food_cons:
                food_items.remove(i)

        return filtered_list
            
            
PRESENT_LOCATION, PRESENT_TIME, PRESENT_SEASON = 123, 2, 1   #Locations of size 300, time of size :4, morning, afternoon, evening, night, season of size :3, summer, rainy, winter    
TRACKER_TIME = datetime.now()
never_ask = 0
class PreferenceFilter:
    
    
    PREF_MODEL = dict()
    def __init__(self, preferred_foods, food_allergies=[], model_id=None):
        global TRACKER_TIME
        
        self.pref_food = preferred_foods
        self.pref_model = self.__make_model()
        self.food_allergies=food_allergies
        self.vocab = self.__make_vocab()
        x, y = self.__preprocess()
        if (TRACKER_TIME + timedelta(hours=2) )<= datetime.now() or (model_id not in PreferenceFilter.PREF_MODEL):
            print(f"Prepping or Updating the model for user with id : {model_id}")
            self.pref_model = self.__train(x, y, eps=100)
            TRACKER_TIME = datetime.now()
            PreferenceFilter.PREF_MODEL[model_id] = self.pref_model
        else:
            print(f"Using stored model for user with id : {model_id}")
            self.pref_model = PreferenceFilter.PREF_MODEL[model_id]
        
    def __make_vocab(self):
        objs = Food.objects.all()
        ingredients = set()
        for fo in objs:
            ingredients.add(fo.key_ingredient1.lower())
            ingredients.add(fo.key_ingredient2.lower())
            ingredients.add(fo.key_ingredient3.lower())
            ingredients.add(fo.key_ingredient4.lower())
            ingredients.add(fo.key_ingredient5.lower())
        ingredients = list(ingredients)
        vocab = {k:v for v,k in enumerate(ingredients)}
        return vocab
        
    def __make_model(self):
        Xinp = Input((5,))  #8 Features : Key Ingredients (1-5), Location(1), Time(1), Season(1) 
        X = Dense(10, activation='relu')(Xinp)
        X = Dense(5, activation='sigmoid')(X)
        X = Dense(1, activation='sigmoid')(X) #One Binary Output mentioning whether user likes the dish or not
        
        model = Model(inputs=Xinp, outputs=X)
        model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
        self.pref_model = model
        return model
    
    def __preprocess(self, xinp=None):
        if type(xinp) == type(None):
            x = []
            y = []
            for fi in self.pref_food:
                x.append([self.vocab[fi.key_ingredient1.lower()], self.vocab[fi.key_ingredient2.lower()], self.vocab[fi.key_ingredient3.lower()], self.vocab[fi.key_ingredient4.lower()], self.vocab[fi.key_ingredient5.lower()]])
                #PRESENT_LOCATION, PRESENT_TIME, PRESENT_SEASON
                y.append(1)
            #negative samples
            xn = []
            yn = []
            for fi in Food.objects.all():
                if fi not in self.pref_food:
                    xn.append([self.vocab[fi.key_ingredient1.lower()], self.vocab[fi.key_ingredient2.lower()], self.vocab[fi.key_ingredient3.lower()], self.vocab[fi.key_ingredient4.lower()], self.vocab[fi.key_ingredient5.lower()]])
                    yn.append(0)
            x += xn
            y += yn
            return np.array(x), np.array(y) 
        else:
            x = []
            for fi in xinp:
                x.append([self.vocab[fi.key_ingredient1.lower()], self.vocab[fi.key_ingredient2.lower()], self.vocab[fi.key_ingredient3.lower()], self.vocab[fi.key_ingredient4.lower()], self.vocab[fi.key_ingredient5.lower()]])
            return np.array(x)
    
    def __eliminate_allergic_foods(self, xinp):
        xinp_new = {k:[] for k in xinp.keys()}
        for k in xinp.keys():
            for fd in xinp[k]:
                if fd.food_name in self.food_allergies or fd.key_ingredient1 in self.food_allergies or fd.key_ingredient2 in self.food_allergies or fd.key_ingredient3 in self.food_allergies or fd.key_ingredient4 in self.food_allergies or fd.key_ingredient5 in self.food_allergies:
                    pass
                else:
                    xinp_new[k] += [fd]
        return xinp_new
    
    def __train(self, x, y, eps=100):
        model = self.pref_model
        model.fit(x, y, epochs=eps, verbose=0)
        self.pref_model = model
        return model
    def __call__(self, xinp):
        
        xinp = self.__eliminate_allergic_foods(xinp)
        filtered_list2 = {k:[] for k in xinp.keys()}
        for fi in filtered_list2.keys():
            xtest = self.__preprocess(xinp[fi])
            if xtest.shape[0] != 0:
                filtered_foods = [xinp[fi][i] for i, v in enumerate(np.sort(self.pref_model(xtest))[::-1]) if v>=0.4]  #considering only interested foods
            else:
                filtered_foods = []
            filtered_list2[fi] += filtered_foods
        return filtered_list2

class MedicalFilter:
    def __init__(self, chronic_illness=[], mineral_deficiency=[], food_allergies=[]):
        self.chronic_illness = chronic_illness
        self.mineral_deficiency = mineral_deficiency
        self.food_allergies = food_allergies
        
    def __eliminate_allergic_foods(self, xinp):
        xinp_new = [] #{k:[] for k in xinp.keys()}
        for fd in xinp:
            if fd.name in self.food_allergies or fd.keing1 in self.food_allergies or fd.keing2 in self.food_allergies or fd.keing3 in self.food_allergies or fd.keing4 in self.food_allergies or fd.keing5 in self.food_allergies:
                pass
            else:
                xinp_new += [fd]
        return xinp_new
    
    def __call__(self, xinp):
        suggest = []
        all_illness_prescriptions = []  #List of all the prescriptions from database available also perform allergy food removal
        for pr in all_illness_prescriptions:
            if pr.illness in self.chronic_illness:
                suggest.append(pr.remedy)
        
        xinp['Chronic Illness Remedies'] = suggest
        
        suggest = []
        all_deficiency_prescriptions = []  #List of all the prescriptions from database available also perform allergy food removal
        for pr in all_deficiency_prescriptions:
            if pr.deficiency in self.mineral_deficiency:
                suggest.append(pr.remedy)
        
        xinp['Mineral Deficiecny Remedies'] = suggest
        
        return xinp
    
def get_homepage(request):
    
    try:
        usr_id, height, weight, cal_intake, act_type, user_name = request.POST['id'], request.POST['height'], request.POST['weight'], request.POST['cal_intake'], request.POST['act_type'], request.POST['user_name']
        height, weight = float(height), float(weight)
    except:
        print("Error caused!, assumption : logging in as regular user ... ")
        act_type= "reg"
        
    fi = list(Food.objects.all())
        
    if (TRACKER_TIME + timedelta(hours=2) )<= datetime.now() or (TRACKER_TIME == datetime.now()):
        res = requests.post('http://127.0.0.1:8000/review/extract_ratings/')
    
    if act_type == 'prem':
        
        if (TRACKER_TIME + timedelta(minutes=2) )<= datetime.now() or (TRACKER_TIME == datetime.now()):
            res = requests.post('http://127.0.0.1:8000/orders/extract_and_dump_food_interests/')
            
        preferred_foods = PreferredFood.objects.raw('select id, pfood_id from user_preferredfood where user_id = %s',[usr_id])
        
        allergy_foods = AllergyFood.objects.raw('select id, afood from user_allergyfood where user_id = %s',[usr_id])
        
        preferred_foods = [pf.pfood for pf in preferred_foods]
        allergy_foods = [af.afood for af in allergy_foods]
        
        bmi_filt = BMIFilter(height/100, weight, float(cal_intake), strict_diet=False)
        
        
        filts = bmi_filt(fi, topn=20)
        if Order.objects.filter(usr_id=usr_id).values('food_id').distinct().count() >=20:
            pref_filt = PreferenceFilter(preferred_foods, food_allergies=allergy_foods, model_id=usr_id)
            filtss = pref_filt(filts)
            flag = 0
            for v in filtss.values():
                if len(v) >0:
                    flag = 1
                    break
            if flag:
                filts = filtss
            else:
                print("Preferred Foods Quantity is not sufficient to determine the personal interests ...")
                
        else:
            print(f"No Enough Orders for user {user_name} to Provide Preference Recommendations ...")
        
        for k, food_objs in filts.items():
            li = []
            for fo in food_objs:
                li.append((fo.food_name, fo.carbs, fo.proteins, fo.fats, fo.key_ingredient1, fo.key_ingredient2, fo.key_ingredient3, fo.key_ingredient4, fo.key_ingredient5, fo.image_path, fo.item_rating, fo.id))
            filts[k] = sorted(li, key = lambda x: x[10], reverse=True)
    else:
        
        rest_fo = dict()
        for fo in fi:
            matchh = re.match('.*(([A-Z])_)[0-9]{2}.jpg', fo.image_path)
            rest_name = matchh.group(2)
            if rest_name not in rest_fo:
                rest_fo[rest_name] = sorted([(foo.food_name, foo.carbs, foo.proteins, foo.fats, foo.key_ingredient1, foo.key_ingredient2, foo.key_ingredient3, foo.key_ingredient4, foo.key_ingredient5, foo.image_path, foo.item_rating, foo.id) for foo in Food.objects.filter(image_path__contains=matchh.group(1))], key=lambda x: x[10], reverse=True)
        filts = rest_fo
    
    return JsonResponse(filts, safe=False)
    