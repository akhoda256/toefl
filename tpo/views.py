from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from .models import Paragraph
from .models import Passage
from .models import Question

from django.http import JsonResponse
from django.http import HttpResponseRedirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def reading(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    print request
    data = {}
    data['passage_title'] = 1
    paragraphs = Paragraph.objects.all().filter(passage__passageNumber__exact=data['passage_title']).order_by('orderingNumber')
    print paragraphs
    return render_to_response('tpo/reading.html', {'paragraphs': paragraphs})
	
@csrf_exempt
def index(request):
    #return HttpResponse("index, world. You're at the polls index.")
    #form = ReportForm()
    return render_to_response('tpo/base.html', {})

@csrf_exempt
def passageText(request, tpoNumber, passageNumber):
    #return HttpResponse("Hello, world. You're at the polls index.")
    tpoNum = int(tpoNumber[:len(tpoNumber)-1])
    passageNum = int(passageNumber[:len(passageNumber) - 1])
    passage = Passage.objects.get(tpo__title__exact=tpoNum, passageNumber=passageNum)
    paragraphs = Paragraph.objects.all().filter(passage__tpo__title__exact=tpoNum)
    paragraphs = paragraphs.filter(passage__passageNumber__exact=passageNum).order_by('orderingNumber')
    return render_to_response('tpo/reading.html', {'paragraphs': paragraphs, 'tpoNum': tpoNum, 'passage': passage})



@csrf_exempt
def getQuestion(request):
    questionNum = request.POST.get('questionNumber', None)
    tpoNum = request.POST.get('tpoNumber', None)
    passageNum = request.POST.get('passageNumber', None)
    question = Question.objects.get(questionNumber=questionNum, paragraph__passage__passageNumber=passageNum, paragraph__passage__tpo__title=tpoNum)
    data = {
        'questionText': question.text
    }
    print JsonResponse(data)
    return JsonResponse(data)