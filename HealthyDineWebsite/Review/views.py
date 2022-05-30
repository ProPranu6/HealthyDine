from django.shortcuts import render

# Create your views here.

from Food.models import Food
from .models import Review



DUMP_NOW = 0
DELETE_NOW = 0
EXTRACT_RATINGS = 0

def dump_reviews():
    print("dumping now ... ")
    revs = [["discrete", "",3],["discrete", " ",5],["discrete", " ", 3],["discrete", " ", 3],["discrete", " ", 5]
,["discrete", " ", 3],["discrete", " ", 5],["discrete", " ", 4],["discrete", " ", 5],["discrete", " ", 4],["discrete", " ", 1],["discrete", " ", 3],["discrete"," ", 4],["discrete", " ", 5],["discrete", "", 2],["discrete", "", 1], ["discrete", " ",3],["discrete", "", 3],["discrete", "", 3],["discrete", "", 4],["discrete", "", 3], ["discrete", "",5],["discrete", "", 2],["discrete", "", 4],["discrete", " ",5],["discrete", " ", 5],["discrete", "", 1],["discrete", "", 2],["discrete", "", 3],["discrete", "", 4],["discrete", "", 2],["discrete", "", 4],["discrete", "", 4], ["discrete", "",4],["discrete", "", 4],["discrete", "", 2],["discrete", "", 5],["discrete", "", 1],["discrete", "", 4],["discrete", "", 5],["descriptive", "I think this is a great food deserves best rating",None],["descriptive","I like this Food I will refer everyone I know",None],
["descriptive","I do not like this Food",None],
["descriptive","There is always something at Healthy Dine that I just have to have!",None],
["descriptive","Would definitely recommend Healthy Dine and will definitely be ordering again",None],
["descriptive","I just love the food items so much - I can come to Healthy Dine, get great service",None],
["descriptive","Very bad Food",None],
["descriptive","Thanks Healthy Dine your food items are amazing and your service is wonderful ",None],
["descriptive","worst Food ever!",None],
["descriptive","can be improved",None]
           ]
    all_objs = Food.objects.all()
    
    for obj in range(len(all_objs)):
        
        if revs[obj][0] == "descriptive":
            Review.objects.create(rev_type=revs[obj][0], rev_content=revs[obj][1], food_id=all_objs[obj].id)
        else:
            Review.objects.create(rev_type=revs[obj][0], rev_rating=revs[obj][2], food_id=all_objs[obj].id)
    return 

if DUMP_NOW:
    dump_reviews()
    
if DELETE_NOW:
    print("deleting now ... ")
    Review.objects.all().delete()
if EXTRACT_RATINGS:
    print("extracting food ratings ... ")
    for fo in Food.objects.all():
        fo.get_overall_rating(Review.objects.all())
    
def extract_ratings(request):
    print("extracting food ratings ... ")
    res = 1
    for fo in Food.objects.all():
        fo.get_overall_rating(Review.objects.all())
    return JsonResponse(1)
    