from django.http import HttpResponse
from django.shortcuts import render


def main(request):
    return HttpResponse('Usage: 127.0.0.1:8000/&ltINSERT QUERY HERE&gt')