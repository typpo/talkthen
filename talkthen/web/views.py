from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist

def index(request):
  context = {}
  return render(request, 'index.html', context)
