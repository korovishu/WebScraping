from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime, date
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from .forms import HandleForm
import simplejson
import requests
# Create your views here.
def home(request):
    if request.method == 'POST':
        form = HandleForm(request.POST)
        if form.is_valid():
            handle = form.cleaned_data.get('handle') 
            return redirect('/stalk/' + handle)
    else:
        form = HandleForm()

    return render(request, 'homepage/home.html', {'form': form})

def stalk(request, handle):
    context = {
        'handle': handle,
    }
    return render(request, 'homepage/stalk.html', context)

def submission_statistics(request, handle):
    friend = handle
    p_link = "https://codeforces.com/api/user.status?handle="
    r = requests.get(p_link + friend)
    data = r.json()
    accepted = 0
    wrong_answer = 0
    time_exceed = 0
    runtime_error = 0
    hacked = 0
    compilation_error = 0
    submissions = {}
    li = []
    for rows in data['result']:
        time = rows['creationTimeSeconds']
        p_date = datetime.fromtimestamp(time).date()
        p_date = p_date.strftime('%Y%m%d')
        print(p_date)
        if submissions.get(p_date) is None:
            submissions[p_date] = 1
        else:
            submissions[p_date] += 1
        if rows.get('verdict') is not None:
            verdict = rows['verdict']
            if verdict == "OK":
                accepted += 1
            elif verdict == "HACKED":
                hacked += 1
            elif verdict == "WRONG_ANSWER":
                wrong_answer += 1
            elif verdict == "TIME_LIMIT_EXCEEDED":
                time_exceed += 1
            elif verdict == "RUNTIME_ERROR":
                runtime_error += 1
            else:
                compilation_error += 1
        json_list = simplejson.dumps(submissions)

    context = {
        'handle': handle,
        'accepted': accepted,
        'hacked': hacked,
        'runtime_error': runtime_error,
        'wrong_answer': wrong_answer,
        'time_exceed': time_exceed,
        'compilation_error': compilation_error,
        'submissions': submissions,
        'json_list': json_list
    }
    return render(request, "homepage/submission_statistics.html", context)


def contest_statistics(request, handle):
    page_url = "https://codeforces.com/api/user.rating?handle=" + handle
    r = requests.get(page_url)
    data = r.json()
    contests = []
    ranks = []
    for i in data['result']:
        contests.append(i['contestId'])
        ranks.append(i['rank'])
    context = {
        'handle': handle,
        'contests': contests,
        'ranks': ranks
    }

    return render(request, "homepage/contest_statistics.html", context)
