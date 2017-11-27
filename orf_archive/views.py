from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Oe1Program
from .oe1_download.download import get_filepath
from os.path import getsize


def german_weekday_abbrev(day):
    return ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'][int(float(day.strftime('%w')))]


@login_required(login_url='orf_archive_login')
def index(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        return redirect('day', day=day)
    days = [date.today() - timedelta(days=i) for i in range(1,31)]
    min_day = Oe1Program.objects.all().order_by('t_day')[:1][0].t_day
    max_day = Oe1Program.objects.all().order_by('-t_day')[:1][0].t_day
    days = [day for day in days if day >= min_day and day <= max_day]
    days_ = []
    for day in days:
        days_.append({
            'iso': day.isoformat(),
            'name': day.strftime('%Y-%m-%d') + ' ({})'.format(german_weekday_abbrev(day)),
        })
    context = {
        'days': days_,
        'min_date': min_day.strftime('%Y-%m-%d'),
        'max_date': max_day.strftime('%Y-%m-%d'),
        'yesterday': (date.today() -timedelta(days=1)).strftime('%Y-%m-%d'),
    }
    return render(request, 'index.html', context)


@login_required(login_url='orf_archive_login')
def day(request, day):
    programs = Oe1Program.objects.filter(t_day=day).order_by('orf_id')
    programs_ = []
    for program in programs:
        date_ = program.t_day.isoformat()
        start = program.data.get('scheduledStartISO')
        time = start[11:16]
        programs_.append({
            'time':  time,
            'title': program.data.get('title'),
            'ressort': program.data.get('ressort'),
            'subtitle': program.data.get('subtitle'),
            'description': program.data.get('description'),
            'files': ['/orf_archive/files/oe1/' + date_ + '/' + filename for filename in program.filenames]
        })
    context = {
        'day': day,
        'programs': programs_
    }
    return render(request, 'day.html', context)


def download(request, filename):
    try:
        filepath = get_filepath(str(filename))
        with open(filepath, 'rb') as file:
            response = HttpResponse(file, content_type='audio/mp3')
            response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
            response['Content-Length'] = getsize(filepath)
        return response
    except:
        return redirect('index')
