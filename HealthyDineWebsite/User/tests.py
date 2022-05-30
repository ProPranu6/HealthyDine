from django.test import TestCase, Client
from .views import signup_regular, signup_premium, login
from django.urls import resolve, reverse
from .models import PremiumUser, RegularUser, PreferredFood, AllergyFood
from Food.models import Food
from Review.models import Review
# Create your tests here.

class TestApps(TestCase):
    
    #Tests on Basic URLS in all the apps
    def test_signup_regular_url(self):
        url = reverse('signupreg')
        self.assertEquals(resolve(url).func, signup_regular)
    
    def test_signup_premium_url(self):
        url = reverse('signupprem')
        self.assertEquals(resolve(url).func, signup_premium)
        
    def test_login_url(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)
        
    #Tests on Basic Views in all the apps
    def test_singup_regular_view(self):
        client = Client()
        response = client.get(reverse('signupreg'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_reg.html')
    
    def test_singup_premium_view(self):
        client = Client()
        response = client.get(reverse('signupprem'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_prem.html')
    
    def test_login_success_view(self):
        client = Client()
        response = client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        
    def test_login_failure_view(self):
        client = Client()
        response = client.post(reverse('login'), {'user_id':'Ranjith', 'password':'wsx76edc'})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_error.html')
        
    
    #Tests on Basic Models in all the apps
    def test_premium_user_model(self):
        pu = PremiumUser.objects.create(user_id="Pranu0945", password='wsxedc', mail_id='pranu0945@gmail.com', contact_no=7418529630, height=172, weight=72, location='Guntur')
        self.assertEquals(pu.user_id, 'Pranu0945')
        
    def test_regular_user_model(self):
        ru = RegularUser.objects.create(user_id="Charan238", password='poklm', mail_id='charan238@gmail.com', contact_no=7418529630, location='Venkatagiri')
        self.assertEquals(ru.mail_id, 'charan238@gmail.com')
        
    def test_preferred_food_model(self):
        fo = Food.objects.create(food_name = 'dosa',
    carbs = 23,
    proteins = 12,
    fats = 10,
    key_ingredient1 = 'batter',
    key_ingredient2 = 'oil',
    key_ingredient3 = 'yeast',
    key_ingredient4 = 'salt',
    key_ingredient5 = 'water',
    item_rating = 0.76)
        pf = PreferredFood.objects.create(user_id=3216, pfood=fo)
        self.assertEquals(pf.pfood.food_name, 'dosa')
        
    def test_allergy_food_model(self):
        af = AllergyFood.objects.create(user_id=3271, afood='spinach')
        self.assertEquals(af.afood, 'spinach')
        
    def test_food_model(self):
        fo = Food.objects.create(food_name = 'dosa',
    carbs = 23,
    proteins = 12,
    fats = 10,
    key_ingredient1 = 'batter',
    key_ingredient2 = 'oil',
    key_ingredient3 = 'yeast',
    key_ingredient4 = 'salt',
    key_ingredient5 = 'water',
    item_rating = 0.76)
        self.assertEquals(fo.key_ingredient2, 'oil')
    
    def test_review_model(self):
        rev = Review.objects.create(rev_type = 'discrete',
    rev_rating = 4,
    food_id = 3271)
        self.assertEquals(rev.rev_rating, 4)
        
        
    
    
