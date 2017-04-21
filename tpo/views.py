from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import QueryDict
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from .classes import AnswerHistory
from .classes import State
from .models import Option
from .models import Paragraph
from .models import Passage
from .models import Question

userStates = {}
endTimes = {}


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
    return render_to_response('tpo/base.html', {})


@csrf_exempt
def passageText(request):
    global endTimes
    tpoNum = request.GET.get('tpoNumber', None)
    passageNum = request.GET.get('passageNumber', None)
    passage = Passage.objects.get(tpo__title__exact=tpoNum, passageNumber=passageNum)
    paragraphs = Paragraph.objects.all().filter(passage__tpo__title__exact=tpoNum)
    paragraphs = paragraphs.filter(passage__passageNumber__exact=passageNum).order_by('orderingNumber')
    startTime = datetime.now() + timedelta(hours=1)
    endTime = startTime.strftime("%Y-%m-%d %H:%M:%S")
    # del request.session[str(request.session.session_key)]
    # request.session.modified = True
    key = request.session.session_key
    print(type(key))
    print(type(request.session))
    print(key)
    if key not in endTimes:
        endTimes[key] = endTime
    else:
        endTime = endTimes[key]

    return render_to_response('tpo/reading.html',
                              {'paragraphs': paragraphs, 'tpoNum': tpoNum, 'passage': passage, 'questionNo': 0,
                               'endTime': endTime})


def build_url(*args, **kwargs):
    params = kwargs.pop('params', {})
    url = reverse(*args, **kwargs)
    if not params:
        return url

    qdict = QueryDict('', mutable=True)
    for k in params:
        v = params[k]
        if type(v) is list:
            qdict.setlist(k, v)
        else:
            qdict[k] = v

    return url + '?' + qdict.urlencode()


@csrf_exempt
def getQuestion(request):
    global userStates
    global endTimes
    session_key = request.session.session_key
    if not request.session.exists(session_key):
        s = build_url('tpo:passage', params={'tpoNumber': '1', 'passageNumber': '1'})
        return HttpResponseRedirect(s)
    if session_key not in endTimes:
        s = build_url('tpo:passage', params={'tpoNumber': '1', 'passageNumber': '1'})
        return HttpResponseRedirect(s)
    else:
        endTime = endTimes[session_key]
    if (request.method == 'GET'):
        questionNum = request.GET.get('questionNumber', None)
        tpoNum = request.GET.get('tpoNumber', None)
        passageNum = request.GET.get('passageNumber', None)
    else:
        questionNum = request.POST.get('questionNumber', None)
        tpoNum = request.POST.get('tpoNumber', None)
        passageNum = request.POST.get('passageNumber', None)
        answer = request.POST.get('optradio', None)
        key = session_key
        cAnswer = AnswerHistory()
        cAnswer.questionNum = questionNum
        cAnswer.answer = answer
        cAnswer.passageNum = passageNum
        cAnswer.tpoNum = tpoNum

        if key not in userStates:
            userState = State()
            userStates[key] = userState

        endTime = endTimes[key]

        userState = userStates[key]
        userState.currentQuestion = questionNum
        userState.history = userState.history + [cAnswer]
        userStates[key] = userState

    questionNum = int(questionNum) + 1

    passage = Passage.objects.get(tpo__title__exact=tpoNum, passageNumber=passageNum)

    if questionNum > passage.questionCount:
        passageNum = int(passageNum) + 1
        s = build_url('tpo:passage', params={'tpoNumber': '1', 'passageNumber': passageNum})
        return HttpResponseRedirect(s)

    question = Question.objects.get(questionNumber=questionNum, paragraph__passage__passageNumber=passageNum,
                                    paragraph__passage__tpo__title=tpoNum)

    options = Option.objects.all().filter(question=question).order_by('number').values('text', 'number')

    paragraphs = Paragraph.objects.all().filter(passage__tpo__title__exact=tpoNum)
    paragraphs = paragraphs.filter(passage__passageNumber__exact=passageNum).order_by('orderingNumber')

    return render_to_response('tpo/reading.html',
                              {'tpoNum': tpoNum, 'paragraphs': paragraphs, 'passage': passage, 'question': question,
                               'options': options, 'questionNo': questionNum,
                               'endTime': endTime})

@csrf_exempt
def listeningAudio(request):
    tpoNum = request.GET.get('tpoNumber', None)
    passageNum = request.GET.get('passageNumber', None)
    passage = Passage.objects.get(tpo__title__exact=tpoNum, passageNumber=passageNum)
    paragraphs = Paragraph.objects.all().filter(passage__tpo__title__exact=tpoNum)
    paragraphs = paragraphs.filter(passage__passageNumber__exact=passageNum).order_by('orderingNumber')
    startTime = datetime.now() + timedelta(hours=1)
    endTime = startTime.strftime("%Y-%m-%d %H:%M:%S")
    if not request.session.exists(request.session.session_key):
        request.session.create()
        key = request.session.session_key
        endTimes[key] = endTime

    return render_to_response('tpo/listening.html',
                              {'paragraphs': paragraphs, 'tpoNum': tpoNum, 'passage': passage, 'questionNo': 0,
                               'startTime': endTime})