from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import forum_post, forums,forum_comment
from model_bakery import baker #auto makews the test models
User_model = get_user_model()

class forum_postTests(TestCase):

    def test_forum_can_be_made(self):
        test_forum = baker.make(forums)
        self.assertIsInstance(test_forum, forums)
        self.assertIsNotNone(test_forum.forum_id)

    def test_forum_post_can_be_made(self):
        test_forum = baker.make(forums)
        test_post = baker.make(forum_post)
        self.assertIsInstance(test_post, forum_post)
        self.assertIsNotNone(test_post.post_id)

    def test_that_profanity_banned(self): 
        test_forum = baker.make(forums)
        test_user = baker.make(User_model)
        with self.assertRaises(ValidationError) as cm: #make sure the validation error is raised when making
            test_post = forum_post.objects.create(author=test_user,
                              forum = test_forum,
                              post_text = "fuck you"            
            )
            test_post.full_clean() 
        self.assertIn('post_text', cm.exception.message_dict)
        #self.assertIn('This field cannot be blank.', cm.exception.message_dict['post_text'])
    
    def test_that_comments_can_be_made(self):
        test_forum = baker.make(forums)
        test_post = baker.make(forum_post)
        test_comment = baker.make(forum_comment)
        self.assertIsInstance(test_comment, forum_comment)
        self.assertIsNotNone(test_comment.comment_id)


