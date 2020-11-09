"""promo_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path, include
from promo.views import PromoViewSet, PromoMeListView

promo_create = PromoViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
promo_detail = PromoViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

api_urlpatterns = [
    path("promo/", promo_create, name="promo-list"),
    path("promo/<int:pk>/", promo_detail, name="promo-detail"),
    path("me/promo", PromoMeListView.as_view(), name="promo-me-list"),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^api/", include(api_urlpatterns)),
]
