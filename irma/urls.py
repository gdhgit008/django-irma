"""irmadjangoapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from irma.apis import IrmaApi

urlpatterns = [
    path('start_irma_session/', IrmaApi.start_irma_session, name='start_irma_session'),
    path('get_irma_session_status/', IrmaApi.get_irma_session_status, name='get_irma_session_status'),
    path('perform_irma_session/', IrmaApi.perform_irma_session, name='perform_irma_session'),
    path('test_succeeded_page/', IrmaApi.test_succeeded_page, name='test_succeeded_page'),
    path('test_authorisation_page/', IrmaApi.test_authorisation_page, name='test_authorisation_page')
]