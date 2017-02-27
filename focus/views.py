import logging
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

logger = logging.getLogger("focus")

def index(request):
	logger.info("test logging")
	return HttpResponse("hello")