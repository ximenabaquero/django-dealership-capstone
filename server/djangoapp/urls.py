from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.generic import TemplateView


app_name = 'djangoapp'

urlpatterns = [
    # --- SPA pages (React) ---
    path('', TemplateView.as_view(template_name="index.html")),
    path('about/', TemplateView.as_view(template_name="index.html")),
    path('contact/', TemplateView.as_view(template_name="index.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('dealers/', TemplateView.as_view(template_name="index.html")),

    # --- API endpoints (JSON) ---
    path('login_api/', views.login_user, name='login'),   # <- evita choque con /login/
    path('logout/', views.logout_user, name='logout'),
    path('register_api/', views.register_user, name='register'),

    path('get_dealers/', views.get_dealers, name='get_dealers'),
    path('get_dealers/<str:state>/', views.get_dealers, name='get_dealers_by_state'),
    path('get_dealer/<int:dealer_id>/', views.get_dealer, name='get_dealer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



