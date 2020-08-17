from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('registration', views.signup, name="registration"),
    path('login', views.login, name="login"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('adminPage', views.adminPage, name="adminPage"),
    path('makeAccount', views.makeAccount, name="makeAccount"),
    path('add_first_tree', views.add_first_tree, name="add_first_tree"),
    path('send_gifting', views.send_gifting, name="send_gifting"),
    path('collect_points', views.collect_points, name="collect_points")
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
