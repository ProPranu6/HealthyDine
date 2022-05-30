from django.db import models

# Create your models here.
from transformers import pipeline
                
class ReviewHandler:
    sentiment_analysis = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english")
    reviewer = sentiment_analysis
    
    @classmethod
    def generate_overall_rating(cls, rev_types, revs):
        overall_rating = 0
        for rev_type, rev in zip(rev_types, revs):
            if rev_type == 'descriptive':
                result = cls.reviewer(rev)[0]
                overall_rating += result['score'] if result['label'] == 'POSITIVE' else 1-result['score']
            else:
                overall_rating += (rev - 1)/(4)
        return overall_rating/len(rev_types)
    
    @classmethod
    def set_overall_rating(cls, reviews, fd_id):
        ##connect to database and set the overall rating of restaurants, delivery_personnel and items
        
        #items = list(set([rev.food_id for rev in reviews]))
        item_ratings = []
        rev_types = []
        revs = []
        for rev in reviews:
            if fd_id == rev.food_id:
                rev_types += [rev.rev_type]
                if rev.rev_type == "descriptive":
                    revs += [rev.rev_content]
                else:
                    revs += [rev.rev_rating]
        if len(rev_types) == 0:
            overall_rating = 0
        else:
            overall_rating = cls.generate_overall_rating(rev_types, revs)
        
        
        
        return overall_rating
    
    @classmethod
    def generate_items_rated_list(cls, item_list):
        rated_list = sorted(item_list, key=lambda x: x.rating, reverse=True)
        return rated_list
    
class Food(models.Model):
    food_name = models.CharField(max_length=25)
    carbs = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    key_ingredient1 = models.CharField(max_length=25)
    key_ingredient2 = models.CharField(max_length=25)
    key_ingredient3 = models.CharField(max_length=25)
    key_ingredient4 = models.CharField(max_length=25)
    key_ingredient5 = models.CharField(max_length=25)
    image_path = models.CharField(max_length=50, default='path_to_your_item_images')
    item_rating = models.FloatField()
    
    def get_overall_rating(self, reviews):
        self.item_rating = ReviewHandler.set_overall_rating(reviews,self.id)
        self.save()
        return

        