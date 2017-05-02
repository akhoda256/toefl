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
    tpo = models.ForeignKey(TPO, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=200)
    passageNumber = models.IntegerField(default=1)
    questionCount = models.IntegerField(default=1)

    def __str__(self):
        return str(self.title)


class Paragraph(models.Model):
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, default=None)
    text = models.CharField(max_length=1200)
    orderingNumber = models.IntegerField(default=1)

    def __str__(self):
        return str(self.text)


class QuestionType(models.Model):
    desc = models.CharField(max_length=200)

    def __str__(self):
        return str(self.desc)


class Question(models.Model):
    questionNumber = models.IntegerField(default=1)
    text = models.CharField(max_length=1200)
    questionType = models.ForeignKey(QuestionType, default=None)

    def __str__(self):
        return str(self.text)


class ReadingQuestion(Question):
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, default=None)
    startHighlight = models.IntegerField(default=1, null=True)
    endHighlight = models.IntegerField(default=1, null=True)

    def __str__(self):
        return str(self.text)


class Option(models.Model):
    text = models.CharField(max_length=200)
    number = models.IntegerField(default=1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    isAnswer = models.NullBooleanField()

    def __str__(self):
        return str(self.number)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, default=None)
    answerType = models.BooleanField()

    def __str__(self):
        return str(self.answerType)


class Conversation(models.Model):
    tpo = models.ForeignKey(TPO, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=200)
    convNumber = models.IntegerField(default=1)
    imgFile = models.FileField(upload_to='tpo/static/images/')
    audioFile = models.FileField(upload_to='tpo/static/audio/')

    def __str__(self):
        return str(self.title)


class ListeningQuestion(Question):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, default=None)
    questionAudioFile = models.FileField(upload_to='tpo/static/audio/', null=True)
    preAudioFile = models.FileField(upload_to='tpo/static/audio/', null=True)
    imgFile = models.FileField(upload_to='tpo/static/images/', null=True)

    def __str__(self):
        return str(self.text)


class SpeakingQuestion(Question):
    questionAudioFile = models.FileField(upload_to='tpo/static/audio/', null=True)
    questionDescription = models.FileField(upload_to='tpo/static/audio/', null=True)
    preparationTime = models.IntegerField(default=1)
    responseTime = models.IntegerField(default=1)
    tpo = models.ForeignKey(TPO, on_delete=models.CASCADE, default=None)

class ReadingPartOfQuestion(models.Model):
    text = models.CharField(max_length=500)
    readingTime = models.IntegerField(default=45)

class ReadingPartOfSpeakingQuestion(ReadingPartOfQuestion):
    title = models.CharField(max_length=100)
    sQuestion = models.ForeignKey(SpeakingQuestion, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return str(self.title)

class ListeningPartOfQuestion(models.Model):
    imgFile = models.FileField(upload_to='tpo/static/images/', null=True)
    audioFile = models.FileField(upload_to='tpo/static/audio/', null=True)

class ListeningPartOfSpeakingQuestion(ListeningPartOfQuestion):
    sQuestion = models.ForeignKey(SpeakingQuestion, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return str(self.imgFile.name)

class SpeakingResponse(models.Model):
    user = models.CharField(max_length=200)
    respFile = models.FileField(upload_to='tpo/static/audio/')
    tpoNo = models.IntegerField(default=1)
    questionNo = models.IntegerField(default=1)


    def __str__(self):
        return str(self.user)


class WritingQuestion(Question):
    responseTime = models.IntegerField(default=1)
    tpo = models.ForeignKey(TPO, on_delete=models.CASCADE, default=None)

class ListeningPartOfWritingQuestion(ListeningPartOfQuestion):
    wQuestion = models.ForeignKey(WritingQuestion, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return str(self.imgFile.name)

class ReadingPartOfWritingQuestion(ReadingPartOfQuestion):
    wQuestion = models.ForeignKey(WritingQuestion, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return str(self.text)