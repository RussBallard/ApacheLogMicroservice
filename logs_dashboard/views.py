from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Sum, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from logs_dashboard.models import LogEntry


def main(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        data = LogEntry.objects.all() if not query \
            else LogEntry.objects.filter(Q(ip__icontains=query) | Q(date__icontains=query) |
                                         Q(method__icontains=query) | Q(status_code__icontains=query) |
                                         Q(user_agent__icontains=query) | Q(referrer__icontains=query) |
                                         Q(request_path__icontains=query))

        paginator = Paginator(data, 50)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            'data': posts,
            'ip_count': data.values('ip').annotate(name_count=Count('ip')).order_by('-name_count')[:10],
            'method_count': data.values('method').annotate(name_count=Count('method')).order_by('-name_count'),
            'response_size': data.aggregate(Sum('response_size'))['response_size__sum']
        }
        return render(request, 'main_page.html', context)
    else:
        return JsonResponse({'message': f'{request.method} method is not allowed'})
