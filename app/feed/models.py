import datetime
import random

from django.db import models


class Feed(models.Model):
    forumid = models.CharField(max_length=12)
    name = models.CharField(max_length=32)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ssg = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def date(self):
        if self.created_at.date() == datetime.date.today():
            return self.created_at.strftime("%H:%M")
        return self.created_at.strftime("%Y-%m-%d")

    def view_count(self):
        return random.randint(10000, 99999)

    def url(self):
        return f"/{self.forumid}/{self.id}"


class Reply(models.Model):
    forumid = models.CharField(max_length=12)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="replies")
    name = models.CharField(max_length=32)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def date(self):
        if self.created_at.date() == datetime.date.today():
            return self.created_at.strftime("%H:%M")
        return self.created_at.strftime("%Y-%m-%d")

    class Meta:
        ordering = ["id"]
