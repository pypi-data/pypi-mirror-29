# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, logging, collections
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import ListURL

# Get an instance of a logger
logger = logging.getLogger(__name__)


def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

@csrf_exempt
def paste(request):
    """
    Subscribe to notifications and POST notifications using /paste URL
    Store incoming notifs to sqlite DB
    :return: JsonResponse 200 with whole data
    """

    logger.info("ViewFunction : paste")
    if request.method == 'GET':
        return JsonResponse("GET request not supported for this URL.", status=405)

    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            logger.info("X_FORWARDED_FOR : {0}".format(x_forwarded_for.split(',')[0]))

        ## X_FORWARDED_FOR one was creating problem with from IP address, let's keep an eye it for now.
        ## Butler IP displayed instead of platform IP, REMOTE_ADDR seems to be working fine.

        ip = request.META.get('REMOTE_ADDR')
        logger.info("REMOTE_ADDR ip : {0}".format(ip))
        notif_type = request.META.get('HTTP_X_PATTERN')
        rec = ListURL(ip_add=ip, notif_type=notif_type, data=data)
        rec.save()
        return JsonResponse(data, status=200)

@csrf_exempt
def pick_notif_data(request):
    """
    Query in the DB to return matching notifs, initially meant for Pick notifs
    :param request: IP Address, Notif Type, externalServiceRequestId
    :return: List of notifications matching above 3 params
    """

    ip_addr = request.GET['ip']
    notif_type = request.GET['notif']
    esr_id = request.GET['esr_id']

    # filter the matching rows
    query_data = ListURL.objects.filter(ip_add=ip_addr, notif_type=notif_type,
                               data__contains="u\'externalServiceRequestId\': u\'{0}\'".format(esr_id)).values()

    final_data = []
    for rec in query_data:
        final_data.append(json.dumps(convert(eval(rec['data']))))

    new = json.dumps(final_data)
    new = new.replace("\\", "")

    return HttpResponse(new, content_type="application/json")

@csrf_exempt
def view(request):
    """
    View the whole data on UI using /view URL, changed to 5 days
    :return: Render complete data with a template
    """

    logger.info("ViewFunction : view")
    if request.method == 'POST':
        return JsonResponse("POST request not supported for this URL.", status=405)

    elif request.method == 'GET':
        today = datetime.today()
        one_month = today + timedelta(-30)
        five_days = today + timedelta(-5)
        query_data = ListURL.objects.filter(datetime__gte=one_month).order_by('-datetime').values()
        for record in query_data:
            for k,v in record.iteritems():
                try:
                    temp = convert(eval(v))
                    if k == 'data':     # we need to display it as JSON on the webpage
                        record[k] = json.dumps(temp)
                    else:
                        record[k] = temp
                except:
                    pass

        return render(request, 'viewdata.html', {'data': query_data})

@csrf_exempt
def view_by_ip(request):
    """
    Filter the data for specified IP using /view_by_ip URL
    :param request: IP address
    :return: Render data with a template
    """

    logger.info("ViewFunction : view_by_ip")
    if request.method == 'POST':
        return JsonResponse("POST request not supported for this URL.", status=405)

    elif request.method == 'GET':
        ip_addr = request.GET['ip'].split(',')
        query_data = ListURL.objects.filter(ip_add__in=ip_addr).order_by('-datetime').values()
        for record in query_data:
            for k,v in record.iteritems():
                try:
                    temp = convert(eval(v))
                    if k == 'data':     # we need to diaplsy it as JSON on the webpage
                        record[k] = json.dumps(temp)
                    else:
                        record[k] = temp
                except:
                    pass

        return render(request, 'viewdata.html', {'data': query_data})

