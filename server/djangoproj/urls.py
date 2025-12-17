from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from pathlib import Path


urlpatterns = [
    path('admin/', admin.site.urls),
    # CRA root files (index.html references these at '/...')
    re_path(
        r'^(?P<path>manifest\.json|favicon\.ico|logo192\.png|logo512\.png|robots\.txt)$',
        serve,
        {'document_root': str(Path(settings.BASE_DIR) / 'frontend' / 'build')},
    ),
    # React SPA routes
    path('dealers/', TemplateView.as_view(template_name="index.html")),
    path('dealer/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),
    path('dealer/<int:dealer_id>/',TemplateView.as_view(template_name="index.html")),
    path('postreview/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),
    path('postreview/<int:dealer_id>/',TemplateView.as_view(template_name="index.html")),
    # App routes (API)
    path('djangoapp/', include('djangoapp.urls')),
    # Static template pages
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('', TemplateView.as_view(template_name="Home.html")),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
   
    path('register/', TemplateView.as_view(template_name="index.html")),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
