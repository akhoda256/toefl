from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


# Create your models here.


class TPO(models.Model):
    title = models.IntegerField(default=1)
    text = models.TextField(max_length=200)

    def __str__(self):
        return str(self.title)


class Passage(models.Model):
    tpo = models.ForeignKey(TPO, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    passageNumber = models.IntegerField(default=1)
    questionCount = models.IntegerField(default=1)

    def __str__(self):
        return str(self.title)


class Paragraph(models.Model):
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE)
    text = models.CharField(max_length=1200)
    orderingNumber = models.IntegerField(default=1)

    def __str__(self):
        return str(self.text)


class QuestionType(models.Model):
    desc = models.CharField(max_length=200)

    def __str__(self):
        return str(self.desc)


class Question(models.Model):
    startHighlight = models.IntegerField(default=1)
    endHighlight = models.IntegerField(default=1)
    questionNumber = models.IntegerField(default=1)
    text = models.CharField(max_length=1200)
    questionType = models.ForeignKey(QuestionType, default=0)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text)


class Option(models.Model):
    text = models.CharField(max_length=200)
    number = models.IntegerField(default=1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    isAnswer = models.NullBooleanField()

    def __str__(self):
        return str(self.number)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    answerType = models.BooleanField()

    def __str__(self):
        return str(self.answerType)
