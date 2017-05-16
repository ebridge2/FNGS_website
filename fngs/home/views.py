from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404


def index(request):
	context = {}
	return render(request, 'home/index.html', context)
