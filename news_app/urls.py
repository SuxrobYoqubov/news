from django.urls import path
from .views import news_list, news_detail, homePageView, ContactViewPage,notPage, \
singlePage, HomePageView, ForeignNewsView, LocalNewsView, SportNewsView, TechnologyNewsView

urlpatterns = [
    path('', HomePageView.as_view(), name = 'home_page'),
    path('all/', news_list, name = 'all_news_list'),
    path('<slug:news>/', news_detail, name ='news_detail_page'),
    path("contact-us/", ContactViewPage.as_view(), name="contact_page"),
    path("not_page/", notPage, name="not_page"),
    path("single-page/", singlePage, name="single_page"),
    path('local', LocalNewsView.as_view(), name='local_news_page'),
    path('foreign', ForeignNewsView.as_view(), name='foreign_news_page'),
    path('technology', TechnologyNewsView.as_view(), name='technology_news_page'),
    path('sport', SportNewsView.as_view(), name='sport_news_page'),

]