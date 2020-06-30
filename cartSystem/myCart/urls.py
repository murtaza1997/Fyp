"""cartSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path("", views.basic, name="basic"),
    path("viewpro/<int:myid>", views.home, name="home"),
    # path("ecart",views.index,name="index"),
    path("viewpro/<int:myid>/<int:myid2>", views.subpro, name="subpro"),
    path("addval/", views.add_item_toCart, name='add'),
    path("addlist/", views.addlist, name="ajax.addlist"),
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),

    path("checkLogin/", views.check_login, name='check_login'),
    path("forcheckout/", views.forcheckout, name='ajax.checkout'),
    path("admin_vp/", views.view_admin, name='admin_vp'),
    path("subpro/<int:sub_id>", views.add_to_list, name="addlist"),
    path("get_admin_data/", views.myview, name='ajax.get_admin_data'),
    path("Recommend_item/", views.recommended_items, name='ajax.recommendation'),
    path("viewlist/", views.ViewList_Customer, name='viewlist'),
    path("seedata/", views.view_temp_data, name='ajax.view_temp_data'),
    path("checker/", views.checker, name='checker'),
    path("GetOrderId/", views.f_checker, name='f_checker'),
    path("vieworder/", views.vieworder, name='ajax.view_order'),
    path("searchmap/", views.searchmap, name='searchmap'),
    path("a_searchmap/", views.a_searchmap, name='ajax.a_searchmap'),
    path("map_pro_view/", views.map_pro_view, name='ajax.map_pro_view'),
    path("id_to_list/", views.id_to_list, name='ajax.id_to_list'),
    path("delete_row/", views.delete_row, name='ajax.delete_row'),

    path("make_confirm/", views.make_confirm, name='ajax.make_confirm'),
    path("delete_confirm/", views.delete_confirm, name='delete_confirm'),



    path("prodetails/<int:myid>", views.pro_details, name="prodetails"),




]
