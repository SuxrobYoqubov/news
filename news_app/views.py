from django.shortcuts import render
from django.shortcuts import get_object_or_404,HttpResponse
from hitcount.utils import get_hitcount_model

from news_app.models import News, Category
from django.views.generic import TemplateView, ListView , UpdateView, DeleteView, CreateView
from .forms import ContactForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from news_project.custom_permissions import OnlyLoggedSuperUser
from django.contrib.auth.models import User
from django.db.models import Q
from hitcount.views import HitCountDetailView, HitCountMixin


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
    # Ko'rishlar soni boshi######################################
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk':hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request,hit_count)
    if hit_count_response.hit_counted:
        hits = hits+1
        hitcontext['hit_counted']=hit_count_response.hit_counted
        hitcontext['hit_message']=hit_count_response.hit_message
        hitcontext['total_hits']=hits
    
    # tugashi########################################################
    comments = news.comments.filter(active = True)
    comment_count = comments.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi komment obyektini yaratamiz DB ga saqlamaymiz
            new_comment = comment_form.save(commit = False)
            # shu comment aynan shu xabarga tegishliligini bog'ladik
            new_comment.news = news
            # Izoh egasini surov yuborayotgan userga bog'landi
            new_comment.user = request.user
            # malumotlar bazasiga saqlayiz            
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'news': news,
        'comments':comments,
        'new_comment': new_comment,
        'comment_form':comment_form,
        'comment_count': comment_count,

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
        return render(request, 'news/contact.html', context)
    
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
    
class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status',)
    template_name = 'crud/news_edit.html'
    
class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')
    


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'title_uz', 'title_en', 'title_ru',
              'slug', 'body', 'body_uz', 'body_en', 'body_ru', 'image', 'category', 'status')
    
@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser = True)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultsView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains = query) | Q(body__icontains=query)
            
        )