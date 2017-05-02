from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import QueryDict
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .classes import AnswerHistory
from .classes import State
from .models import Option, ReadingQuestion, ListeningQuestion
from .models import Paragraph
from .models import Passage
from .models import Question
from .models import Conversation

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SpeakingResponseForm
from .models import SpeakingResponse
from .models import SpeakingQuestion
from .models import ReadingPartOfSpeakingQuestion
from .models import ListeningPartOfSpeakingQuestion

from .models import WritingQuestion
from .models import ReadingPartOfWritingQuestion
from .models import ListeningPartOfWritingQuestion

# Imaginary function to handle an uploaded file.

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
def getReadingQuestion(request):
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
    if request.method == 'GET':
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

    question = ReadingQuestion.objects.get(questionNumber=questionNum, paragraph__passage__passageNumber=passageNum,
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
    convNum = request.GET.get('convNumber', None)
    conversation = Conversation.objects.get(tpo__title__exact=tpoNum, convNumber=convNum)
    ind = conversation.imgFile.url.find('/static')
    imgPath = conversation.imgFile.url[ind:]
    ind = conversation.audioFile.url.find('/static')
    audioPath = conversation.audioFile.url[ind:]
    return render_to_response('tpo/listen.html',
                              {'tpoNum': tpoNum, 'conversation': conversation, 'imgPath': imgPath,
                               'audioPath': audioPath})


@csrf_exempt
def listeningQuestion(request):
    tpoNum = request.GET.get('tpoNumber', None)
    convNum = request.GET.get('convNumber', None)
    questionNumber = request.GET.get('questionNumber', None)
    conversation = Conversation.objects.get(tpo__title__exact=tpoNum, convNumber=convNum)
    question = ListeningQuestion.objects.get(questionNumber=questionNumber,
                                             conversation__convNumber=convNum)
    imgPath = None
    is_pre_img = False
    is_pre_audio = False
    if question.imgFile.name is not None:
        ind = question.imgFile.url.find('/static')
        imgPath = question.imgFile.url[ind:]
        is_pre_img = True

    audioPath = None
    if question.questionAudioFile.name is not None:
        ind = question.questionAudioFile.url.find('/static')
        audioPath = question.questionAudioFile.url[ind:]
        if is_pre_img is False:
            is_pre_audio = True

    return render_to_response('tpo/listen.html', {'tpoNum': tpoNum, 'conversation': conversation, 'imgPath': imgPath,
                                                  'audioPath': audioPath, 'is_pre_img': is_pre_img,
                                                  'is_pre_audio': is_pre_audio})


@csrf_exempt
def speakingQuestion(request):
    tpoNum = request.GET.get('tpoNumber', None)
    questionNum = request.GET.get('questionNumber', None)
    partNum = request.GET.get('partNumber', None)
    question = SpeakingQuestion.objects.get(tpo__title__exact=tpoNum, questionNumber=questionNum)
    nextPart = int(partNum) + 1
    if questionNum in ['0', '1']:
        nextPart = '3'
    elif questionNum in ['3', '4']:
        if nextPart == 1:
            nextPart = '2'
    if partNum == '0':
        ind = question.questionDescription.url.find('/static')
        descAudioPath = question.questionDescription.url[ind:]
        return render_to_response('tpo/speaking.html',
                                  {'questionNo': questionNum, 'tpoNum': tpoNum,
                                   'descAudioPath': descAudioPath, 'partNum': partNum, 'nextPart': nextPart})
    elif partNum == '1':
        readingOfQuestion = ReadingPartOfSpeakingQuestion.objects.get(sQuestion__pk=question.pk)
        return render_to_response('tpo/speaking.html',
                                  {'questionNo': questionNum, 'tpoNum': tpoNum, 'question': question,
                                   'readingObj': readingOfQuestion, 'partNum': partNum, 'nextPart': nextPart})
    elif partNum == '2':
        listeningOfQuestion = ListeningPartOfSpeakingQuestion.objects.get(sQuestion__pk=question.pk)
        ind = listeningOfQuestion.imgFile.url.find('/static')
        listeningObjImage = listeningOfQuestion.imgFile.url[ind:]
        ind = listeningOfQuestion.audioFile.url.find('/static')
        listeningObjAudio = listeningOfQuestion.audioFile.url[ind:]
        return render_to_response('tpo/speaking.html',
                                  {'questionNo': questionNum, 'tpoNum': tpoNum, 'question': question,
                                   'listeningObjImage': listeningObjImage, 'listeningObjAudio': listeningObjAudio,
                                   'partNum': partNum, 'nextPart': nextPart})
    else:
        ind = question.questionAudioFile.url.find('/static')
        questionAudioPath = question.questionAudioFile.url[ind:]
        return render_to_response('tpo/speaking.html',
                                  {'questionNo': questionNum, 'tpoNum': tpoNum, 'question': question,
                                   'questionAudioPath': questionAudioPath, 'nextPart': nextPart})


@csrf_exempt
def speakingResponse(request):
    if request.method == 'POST':
        form = SpeakingResponseForm(request.POST, request.FILES)
        if form.is_valid():
            qNo = request.POST.get('questionNo')
            tNo = request.POST.get('tpoNo')
            instance = SpeakingResponse(respFile=request.FILES['respFile'], user=request.POST.get('user'),
                                        questionNo=qNo, tpoNo=request.POST.get('tpoNo'))
            instance.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})
    else:
        form = SpeakingResponseForm()
    return render(request, 'upload.html', {'form': form})


@csrf_exempt
def writingQuestion(request):
    tpoNum = request.GET.get('tpoNumber', None)
    questionNum = request.GET.get('questionNumber', None)
    partNum = request.GET.get('partNumber', None)
    question = WritingQuestion.objects.get(tpo__title__exact=tpoNum, questionNumber=questionNum)
    nextPart = int(partNum) + 1
    if questionNum == '1':
        if partNum == '0':
            readingOfQuestion = ReadingPartOfWritingQuestion.objects.get(wQuestion__pk=question.pk)
            return render_to_response('tpo/writing.html',
                                      {'questionNo': questionNum, 'tpoNum': tpoNum, 'question': question,
                                       'nextPart': nextPart, 'readingOfQuestion': readingOfQuestion,
                                       'partNum': partNum})
        elif partNum == '1':
            listeningOfQuestion = ListeningPartOfWritingQuestion.objects.get(wQuestion__pk=question.pk)
            ind = listeningOfQuestion.imgFile.url.find('/static')
            listeningObjImage = listeningOfQuestion.imgFile.url[ind:]
            ind = listeningOfQuestion.audioFile.url.find('/static')
            listeningObjAudio = listeningOfQuestion.audioFile.url[ind:]
            return render_to_response('tpo/writing.html',
                                      {'questionNo': questionNum, 'tpoNum': tpoNum, 'question': question,
                                       'listeningObjImage': listeningObjImage, 'listeningObjAudio': listeningObjAudio,
                                       'partNum': partNum, 'nextPart': nextPart})
        else:
            readingOfQuestion = ReadingPartOfWritingQuestion.objects.get(wQuestion__pk=question.pk)
            return render_to_response('tpo/writing.html',
                                      {'questionNo': questionNum, 'tpoNum': tpoNum, 'question': question,
                                       'partNum': partNum, 'nextPart': nextPart,
                                       'readingOfQuestion': readingOfQuestion})
    else:
        return render_to_response('tpo/writing.html',
                                  {'questionNo': questionNum, 'tpoNum': tpoNum, 'question': question,
                                   'nextPart': nextPart, 'partNum': partNum})