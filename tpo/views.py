from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from .models import Paragraph
from .models import Passage
from .models import Question
from .models import Option
from django.core import serializers
import uuid
from .classes import State
from .classes import AnswerHistory

from django.http import JsonResponse
from django.http import HttpResponseRedirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

userStates = {}


@csrf_exempt
def reading(request):
    print(request)
    data = {}
    data['passage_title'] = 1
    paragraphs = Paragraph.objects.all().filter(passage__passageNumber__exact=data['passage_title']).order_by(
        'orderingNumber')
    print(paragraphs)
    return render_to_response('tpo/reading.html', {'paragraphs': paragraphs})


@csrf_exempt
def index(request):
    # return HttpResponse("index, world. You're at the polls index.")
    # form = ReportForm()
    return render_to_response('tpo/base.html', {})


@csrf_exempt
def passageText(request, tpoNumber, passageNumber):
    # return HttpResponse("Hello, world. You're at the polls index.")
    tpoNum = int(tpoNumber[:len(tpoNumber) - 1])
    passageNum = int(passageNumber[:len(passageNumber) - 1])
    passage = Passage.objects.get(tpo__title__exact=tpoNum, passageNumber=passageNum)
    paragraphs = Paragraph.objects.all().filter(passage__tpo__title__exact=tpoNum)
    paragraphs = paragraphs.filter(passage__passageNumber__exact=passageNum).order_by('orderingNumber')
    return render_to_response('tpo/reading.html',
                              {'paragraphs': paragraphs, 'tpoNum': tpoNum, 'passage': passage, 'questionNo': 0})


@csrf_exempt
def getQuestion(request):
    global userStates
    if (request.method == 'GET'):
        questionNum = request.GET.get('questionNumber', None)
        tpoNum = request.GET.get('tpoNumber', None)
        passageNum = request.GET.get('passageNumber', None)
    else:
        questionNum = request.POST.get('questionNumber', None)
        tpoNum = request.POST.get('tpoNumber', None)
        passageNum = request.POST.get('passageNumber', None)
        answer = request.POST.get('optradio', None)
        # if 'ak_session_key' not in request.session:
        #     key = uuid.uuid4()
        #     request.session['session_key'] = key
        #
        # key = request.session['session_key']
        if not request.session.exists(request.session.session_key):
            request.session.create()

        key = request.session.session_key
        cAnswer = AnswerHistory()
        cAnswer.questionNum = questionNum
        cAnswer.answer = answer
        cAnswer.passageNum = passageNum
        cAnswer.tpoNum = tpoNum

        if key not in userStates:
            userState = State()
            userStates[key] = userState

        userState = userStates[key]
        userState.currentQuestion = questionNum
        userState.history = userState.history + [cAnswer]
        userStates[key] = userState

        print(answer)

    questionNum = int(questionNum) + 1
    question = Question.objects.get(questionNumber=questionNum, paragraph__passage__passageNumber=passageNum,
                                    paragraph__passage__tpo__title=tpoNum)

    options = Option.objects.all().filter(question=question).order_by('number').values('text', 'number')

    passage = Passage.objects.get(tpo__title__exact=tpoNum, passageNumber=passageNum)
    paragraphs = Paragraph.objects.all().filter(passage__tpo__title__exact=tpoNum)
    paragraphs = paragraphs.filter(passage__passageNumber__exact=passageNum).order_by('orderingNumber')

    return render_to_response('tpo/reading.html',
                              {'tpoNum': tpoNum, 'paragraphs': paragraphs, 'passage': passage, 'question': question,
                               'options': options, 'questionNo': questionNum})
