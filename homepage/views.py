from django.shortcuts import render, redirect, HttpResponse
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from .forms import HandleForm
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

def statistics(request, handle):
    friend = handle
    p_link = "https://codeforces.com/submissions/"
    accepted = 0
    wrong_answer = 0
    time_exceed = 0
    runtime_error = 0
    hacked = 0
    compilation_error = 0
    for i in range(1, 2):
        page_url = p_link + friend + "/page/" + str(i)
        u_client = urlopen(page_url)
        page_soup = soup(u_client.read(), "html.parser")
        u_client.close()
        containers = page_soup.findAll("div", {"class": "datatable"})
        table = containers[0]
        for rows in table.findAll("tr", {"data-submission-id": re.compile(r'\b')}):
            verdict = rows.findAll("td", {"waiting": "false"})
            verdict = verdict[0]
            verdict = verdict.findAll("span")[0]
            if len(verdict.findAll("span")) > 0:
                verdict = verdict.findAll("span")[0].text
                if verdict == "Accepted":
                    accepted += 1
                elif verdict == "Hacked":
                    hacked += 1
                elif re.compile('Wrong answer').match(verdict):
                    wrong_answer += 1
                elif re.compile('Runtime error').match(verdict):
                    runtime_error += 1
                else:
                    time_exceed += 1
            else:
                compilation_error += 1
    context = {
        'handle': handle,
        'accepted': accepted,
        'hacked': hacked,
        'runtime_error': runtime_error,
        'wrong_answer': wrong_answer,
        'time_exceed': time_exceed,
        'compilation_error': compilation_error
    }
    return render(request, "homepage/statistics.html", context)

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