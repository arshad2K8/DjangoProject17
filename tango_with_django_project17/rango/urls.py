__author__ = 'arshad'
from django.conf.urls import patterns,url
from rango import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/', views.about, name='about'),
                       url(r'^add_category/$', views.add_category, name='add_category'),
                       #url(r'^sample_form/$', views.sample_form, name='sample_form'),
                       url(r'^category/(?P<cat_name_slug>[\w\-]+)/$', views.category, name='category'),
)