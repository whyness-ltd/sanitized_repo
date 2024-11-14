#----------------------------------------------------------------------
# Whyness timesheet views
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

import csv
from django.db.models import Sum
from django.http import StreamingHttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from whyness_timesheet.models import Timeentry

# Create your views here.

def timesheets(request):
    """
    Whyness timesheet summary report
    """
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('home'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('home'))
    if not request.user.is_verified:
        return HttpResponseRedirect(reverse('home'))
    timesheets = Timeentry.objects.values('date').annotate(
            Sum('annual_leave'),
            Sum('statutory_holiday'),
            Sum('sick_leave'),
            Sum('hr_recruitment'),
            Sum('design_architecture'),
            Sum('admin_pmo'),
            Sum('comms_marketing'),
            Sum('product_development'),
            Sum('strategy'),
            Sum('user_research'),
            gtotal=Sum('annual_leave')
            + Sum('statutory_holiday')
            + Sum('sick_leave')
            + Sum('hr_recruitment')
            + Sum('design_architecture')
            + Sum('admin_pmo')
            + Sum('comms_marketing')
            + Sum('product_development')
            + Sum('strategy')
            + Sum('user_research'),
        ).order_by('-date')

    context = {
        "timesheets": timesheets,
    }
    return render(request, 'whyness_timesheet/timesheets.html', context)

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def timesheet_csv(request):
    """
    Whyness timesheet summary csv
    """
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('home'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('home'))
    if not request.user.is_verified:
        return HttpResponseRedirect(reverse('home'))
    timesheets = Timeentry.objects.values('date').annotate(
            Sum('annual_leave'),
            Sum('statutory_holiday'),
            Sum('sick_leave'),
            Sum('hr_recruitment'),
            Sum('design_architecture'),
            Sum('admin_pmo'),
            Sum('comms_marketing'),
            Sum('product_development'),
            Sum('strategy'),
            Sum('user_research'),
            gtotal=Sum('annual_leave')
            + Sum('statutory_holiday')
            + Sum('sick_leave')
            + Sum('hr_recruitment')
            + Sum('design_architecture')
            + Sum('admin_pmo')
            + Sum('comms_marketing')
            + Sum('product_development')
            + Sum('strategy')
            + Sum('user_research'),
        ).order_by('-date')

    header = [
        'Date',
        'Total',
        'Recruitment',
        'User research and testing',
        'Market / Customer Research & Engagement, & Strategy',
        'Solution Design and Development',
        'Annual leave',
        'Statutory holiday',
        'Sick leave',
        ]
    rows = (
        ['{}'.format(timesheet['date']),
        '{}'.format(
            timesheet['annual_leave__sum']
            + timesheet['statutory_holiday__sum']
            + timesheet['sick_leave__sum']
            + timesheet['hr_recruitment__sum']
            + timesheet['design_architecture__sum']
            + timesheet['admin_pmo__sum']
            + timesheet['comms_marketing__sum']
            + timesheet['product_development__sum']
            + timesheet['strategy__sum']
            + timesheet['user_research__sum']
        ),
        '{}'.format(timesheet['hr_recruitment__sum']),
        '{}'.format(timesheet['user_research__sum']),
        '{}'.format(timesheet['comms_marketing__sum']),
        '{}'.format(timesheet['design_architecture__sum']),
        '{}'.format(timesheet['annual_leave__sum']),
        '{}'.format(timesheet['statutory_holiday__sum']),
        '{}'.format(timesheet['sick_leave__sum']),
        ] for timesheet in timesheets)
    pseudo_buffer = Echo()
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="timesheet.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)
    return response

def timesheet_detail_csv(request):
    """
    Whyness timesheet detail csv
    """
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('home'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('home'))
    timesheets = Timeentry.objects.all().order_by('-date')

    header = [
        'Date',
        'Employee',
        'Total',
        'Recruitment',
        'User research and testing',
        'Market / Customer Research & Engagement, & Strategy',
        'Solution Design and Development',
        'Annual leave',
        'Statutory holiday',
        'Sick leave',
        ]
    rows = (
        ['{}'.format(timesheet.date),
        '{}'.format(timesheet.user.first_name + ' ' + timesheet.user.last_name),
        '{}'.format(
            timesheet.annual_leave
            + timesheet.statutory_holiday
            + timesheet.sick_leave
            + timesheet.hr_recruitment
            + timesheet.design_architecture
            + timesheet.admin_pmo
            + timesheet.comms_marketing
            + timesheet.product_development
            + timesheet.strategy
            + timesheet.user_research
        ),
        '{}'.format(timesheet.hr_recruitment),
        '{}'.format(timesheet.user_research),
        '{}'.format(timesheet.comms_marketing),
        '{}'.format(timesheet.design_architecture),
        '{}'.format(timesheet.annual_leave),
        '{}'.format(timesheet.statutory_holiday),
        '{}'.format(timesheet.sick_leave),
        ] for timesheet in timesheets)
    pseudo_buffer = Echo()
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="timesheet-detail.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)
    return response
