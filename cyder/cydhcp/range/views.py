import json

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

import ipaddr

from cyder.base.utils import make_paginator, tablefy
from cyder.core.ctnr.models import Ctnr
from cyder.cydhcp.constants import *
from cyder.cydhcp.range.models import Range, RangeKeyValue
from cyder.cydhcp.range.range_usage import range_usage
from cyder.cydhcp.utils import two_to_one
from cyder.cydhcp.vrf.models import Vrf
from cyder.cydns.ip.models import ipv6_to_longs


def delete_range_attr(request, attr_pk):
    """
    An view destined to be called by ajax to remove an attr.
    """
    attr = get_object_or_404(RangeKeyValue, pk=attr_pk)
    attr.delete()
    return HttpResponse("Attribute Removed.")


def range_detail(request, pk):
    mrange = get_object_or_404(Range, pk=pk)

    allow = None
    if mrange.allow == ALLOW_OPTION_VRF:
        try:
            allow = [Vrf.objects.get(network=mrange.network)]
        except ObjectDoesNotExist:
            allow = []
    elif mrange.allow == ALLOW_OPTION_KNOWN:
        allow = [ALLOW_OPTION_KNOWN]
    elif mrange.allow == ALLOW_OPTION_LEGACY:
        allow = [ctnr for ctnr in Ctnr.objects.filter(ranges=mrange)]

    start_upper = mrange.start_upper
    start_lower = mrange.start_lower
    end_upper = mrange.end_upper
    end_lower = mrange.end_lower
    range_data, ip_usage_percent = range_usage(
        two_to_one(start_upper, start_lower),
        two_to_one(end_upper, end_lower),
        mrange.ip_type)
    return render(request, 'range/range_detail.html', {
        'obj': mrange,
        'obj_type': 'range',
        'ranges_table': tablefy((mrange,)),
        'range_data': make_paginator(request, range_data, 50),
        'attrs_table': tablefy(mrange.rangekeyvalue_set.all()),
        'allow_list': allow,
        'range_used': "{0}%".format(ip_usage_percent)
    })


def redirect_to_range_from_ip(request):
    ip_str = request.GET.get('ip_str')
    ip_type = request.GET.get('ip_type')
    if not (ip_str and ip_type):
        return HttpResponse(json.dumps({'failure': "Slob"}))

    if ip_type == '4':
        try:
            ip_upper, ip_lower = 0, int(ipaddr.IPv4Address(ip_str))
        except ipaddr.AddressValueError:
            return HttpResponse(json.dumps(
                {'success': False,
                 'message': "Failure to recognize {0} as an IPv4 "
                            "Address.".format(ip_str)}))
    else:
        try:
            ip_upper, ip_lower = ipv6_to_longs(ip_str)
        except ValidationError:
            return HttpResponse(json.dumps({'success': False,
                                            'message': 'Invalid IP'}))

    range_ = Range.objects.filter(
        start_upper__lte=ip_upper, start_lower__lte=ip_lower,
        end_upper__gte=ip_upper, end_lower__gte=ip_lower)
    if not len(range_) == 1:
        return HttpResponse(json.dumps({'failure': "Failture to find range"}))
    else:
        return HttpResponse(json.dumps(
            {'success': True,
             'redirect_url': range_[0].get_detail_url()}))
