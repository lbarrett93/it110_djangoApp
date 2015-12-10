import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)
	
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
	time = timezone.now() - datetime.timedelta(days=30)
	old_question = Question(pub_date=time)
	self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
	"""
	was_published_recently() should return True for questions whose
	pub_date is within the last day.
    	"""
	time = timezone.now() - datetime.timedelta(hours=1)
	recent_question = Question(pub_date=time)
	self.assertEqual(recent_question.was_published_recently(), True)

class QuestionIndexDetailTests(TestCase):
    
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        response = self.client.get(reverse('polls:detail',
                                   args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question(question_text='Past Question.',days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text,status_code=200)
