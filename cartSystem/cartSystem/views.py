from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import json
from itertools import combinations
from math import ceil
from django.contrib.sessions.models import Session
from django.contrib.auth import logout
import pyodbc


def index(request):
    return render(request, 'myCart/Start.html')
