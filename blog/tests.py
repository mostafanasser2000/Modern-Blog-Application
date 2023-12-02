from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post
from .models import Category
# Create your tests here.
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            username='test_user', email='test@gmail.com', password='secret'
        )
        
        cls.category = Category.objects.create(title='test category')
        
        cls.post = Post.objects.create(
            title='test title', 
            content='test content',
            author = cls.user,
            # categories = cls.category,
        )
        
        
    def test_post_model(self):
        self.assertEqual(self.post.title, 'test title')
        self.assertEqual(self.post.content, 'test content')
        self.assertEqual(self.post.author.username, 'test_user')
        self.assertEqual(str(self.post), 'test title')
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')

    
    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
    
    
    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get('/post/1/')
        self.assertEqual(response.status_code, 200)
    
    
    def test_post_listview(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
    
    
def test_post_detailview(self):
    response = self.client.get(reverse("post_detail", kwargs={"id": self.pk}))
    no_response = self.client.get(reverse("post_detail", kwargs={"id": 1000}))
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(no_response.status_code, 204)
    self.assertTemplateUsed(response, "post_detail.html")

    