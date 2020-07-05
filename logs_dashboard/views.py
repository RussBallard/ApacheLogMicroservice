from datetime import datetime

import xlwt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Sum, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from logs_dashboard.models import LogEntry


@csrf_exempt
def main_dashboard(request):
    query = request.GET.get('q', '')
    data = LogEntry.objects.all() if not query \
        else LogEntry.objects.filter(Q(ip__icontains=query) | Q(date__icontains=query) |
                                     Q(method__icontains=query) | Q(status_code__icontains=query) |
                                     Q(user_agent__icontains=query) | Q(referrer__icontains=query) |
                                     Q(request_path__icontains=query))

    if request.method == 'POST':
        response = excel_export(data)
        return response

    elif request.method == 'GET':
        page = request.GET.get('page')
        context = main_page_data(page, data)
        return render(request, 'main_page.html', context)

    else:
        return JsonResponse({'message': f'{request.method} method is not allowed'})


def excel_export(data):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Export LogEntry {}.xlsx'.format(
        datetime.now().strftime('%d-%m-%Y_%H:%M:%S'))

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Log Entry')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['ID', 'IP', 'DATE', 'METHOD', 'REQUEST PATH', 'HTTP VERSION',
               'STATUS CODE', 'RESPONSE SIZE', 'REFERRER', 'USER AGENT']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    for row in data.values_list():
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response


def main_page_data(page, data):
    paginator = Paginator(data, 50)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return {
        'data': posts,
        'ip_count': data.values('ip').annotate(name_count=Count('ip')).order_by('-name_count')[:10],
        'method_count': data.values('method').annotate(name_count=Count('method')).order_by('-name_count'),
        'response_size': data.aggregate(Sum('response_size'))['response_size__sum'] or 0
    }
