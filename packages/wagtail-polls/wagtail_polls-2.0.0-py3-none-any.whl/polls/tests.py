from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .models import Poll, PollItem, Vote


class TestPolls(APITestCase):
    def create_poll(self):
        return Poll.objects.create(name="test", message="testing")

    def test_polls_list(self):
        url = reverse('polls-list')
        poll = self.create_poll()
        res = self.client.get(url)
        self.assertContains(res, poll.name)

    def test_vote(self):
        url = reverse('vote-list')
        poll = self.create_poll()
        item = PollItem.objects.create(poll=poll, message="1")
        user = User.objects.create_user(
            username="test", email="test@example.com", password="test")

        self.client.force_authenticate(user=user)
        data = {'item': item.id}
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 201)
        votes = Vote.objects.filter(user=user)
        self.assertEqual(votes.count(), 1)

        # One vote per poll
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 400)
        votes = Vote.objects.filter(user=user)
        self.assertEqual(votes.count(), 1)

        poll2 = Poll.objects.create(name="test2", message="testing")
        item2 = PollItem.objects.create(poll=poll2, message="2")
        data = {'item': item2.id}
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 201)
        votes = Vote.objects.filter(user=user)
        self.assertEqual(votes.count(), 2)
