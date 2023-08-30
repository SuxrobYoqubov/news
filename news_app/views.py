from django.shortcuts import render
from django.shortcuts import get_object_or_404,HttpResponse
from news_app.models import News, Category
from django.views.generic import TemplateView, ListView
from .forms import ContactForm
# Create your views here.

def news_list(request):
    #news_list = News.objects.filter(status = News.Status.Published)
    news_list = News.published.all()
    context = {
        'news_list':news_list
    }
    return render(request, 'news/news_list.html', context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status = News.Status.Published)
    context = {
        'news': news,

    }
    return render(request,'news/news_detail.html', context = context)

def homePageView(requests):
    categories = Category.objects.all()
    news_list = News.published.all().order_by('-publish_time')[:15]
    local_one = News.published.filter(category__name = "Mahalliy").order_by('-publish_time')[0:1]
    local_news = News.published.all().filter(category__name = "Mahalliy").order_by('-publish_time')[1:6]
    context = {
        'news_list':news_list,
        'categories':categories,
        'local_one':local_one,
        'local_news':local_news,
    }
    return render(requests, 'news/home.html', context)

class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['mahalliy_xabarlar'] = News.published.all().filter(category__name = "Mahalliy").order_by('-publish_time')[:5]
        context['xorij_xabarlar'] = News.published.all().filter(category__name = "Xorij").order_by('-publish_time')[:5]
        context['sport_xabarlar'] = News.published.all().filter(category__name = "Sport").order_by('-publish_time')[:5]
        context['texnalogiya_xabarlar'] = News.published.all().filter(category__name = "Texnalogiya").order_by('-publish_time')[:5]
        return context



# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse("<h2>Biz bilan bog'langaniz uchun tashakkur</h2>")
#     else:
#         return HttpResponse("<h2>Ma'lumotlar to'liq emas</h2>")
#     context = {
#         'form':form
#     }
#     return render(request, 'news/contact.html', context)


def notPage(request):
    context = {
        
    }
    return render(request, 'news/404.html', context)


def singlePage(request):
    context = {
        
    }
    return render(request, 'news/single_page.html', context)

class ContactViewPage(TemplateView):
    template_name = 'news/contact.html'
    
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form':form
        }
        return render(request, 'new/contact.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bog'langaniz uchun tashakkur</h2>")
        context = {
            'form':form
        }
        return render(request, 'news/contact.html', context)
    
class LocalNewsView(ListView):
    model= News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'
    
    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'Mahalliy')
        return news
        
    
class ForeignNewsView(ListView):
    model= News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'
    
    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'Xorij')
        return news
    
class TechnologyNewsView(ListView):
    model= News
    template_name = 'news/texnalogiya.html'
    context_object_name = 'texnalogiya_yangiliklar'
    
    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'Texnalogiya')
        return news
    
class SportNewsView(ListView):
    model= News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'
    
    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'Sport')
        return news