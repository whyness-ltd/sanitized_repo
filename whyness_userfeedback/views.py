#----------------------------------------------------------------------
# Whyness User feedback views
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
from django.db import connection
from django.contrib.flatpages.models import FlatPage
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from whyness_django.models import AuthUser
from whyness_django.views import get_host_info, get_useragent

from whyness_userfeedback.forms import SweetSpotForm

from whyness_userfeedback.models import SweetSpot
from whyness_userfeedback.models import SweetSpotValue
from whyness_userfeedback.models import SweetSpotStrength
from whyness_userfeedback.models import SweetSpotImpact
from whyness_userfeedback.models import SweetSpotConfidence
from whyness_userfeedback.models import STATUS_ACTIVE

def userfeedback(request, xref):
    """
    Whyness user feedback
    """
    try:
        user = AuthUser.objects.get(xref=xref)
    except AuthUser.DoesNotExist:
        raise Http404

    values = SweetSpotValue.objects.filter(status=STATUS_ACTIVE)
    strengths = SweetSpotStrength.objects.filter(status=STATUS_ACTIVE)
    impacts = SweetSpotImpact.objects.filter(status=STATUS_ACTIVE)
    confidences = SweetSpotConfidence.objects.filter(status=STATUS_ACTIVE)
    feedback_intro = FlatPage.objects.get(url="/userfeedback/intro/")
    feedback_thankyou = FlatPage.objects.get(url="/userfeedback/thankyou/")
    form = None
    if request.method == 'POST':
        useragent = get_useragent(request)
        (remote_addr, remote_host) = get_host_info(request)
        instance = SweetSpot(
            user=user,
            ip=remote_addr,
            useragent=useragent,
        )
        form = SweetSpotForm(request.POST, instance=instance)
        form.save()
    else:
        form = SweetSpotForm()

    context = {
        "values": values,
        "strengths": strengths,
        "impacts": impacts,
        "confidences": confidences,
        'feedback_intro': feedback_intro,
        'feedback_thankyou': feedback_thankyou,
        "form": form,
        "user": user,
    }
    return render(request, 'whyness_userfeedback/userfeedback.html', context)

def feedback_summary(request):
    """
    Whyness feedback summary
    """
    if not request.user.is_staff:
        raise Http404
    if not request.user.is_verified:
        return HttpResponseRedirect(reverse('home'))

    raw_sql = """SELECT
    u.name, u.email, count(ss.id),
    min(date(ss.create_date)) AS earliest,
    max(date(ss.create_date)) AS latest
    FROM whyness_userfeedback_sweetspot AS ss
    INNER JOIN whyness_django_authuser AS u
    ON ss.user_id = u.id
    GROUP BY u.id
    ORDER BY u.email"""

    with connection.cursor() as cursor:
        cursor.execute(raw_sql)
        custom_columns = [col[0] for col in cursor.description]
        custom_result = cursor.fetchall()
    context = {
        'custom_result': custom_result,
        'custom_columns': custom_columns,
    }
    template = 'whyness_userfeedback/feedback_summary.html'
    return render(request, template, context)

