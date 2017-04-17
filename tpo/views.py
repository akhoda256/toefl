from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from .models import Paragraph
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