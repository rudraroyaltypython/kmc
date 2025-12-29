from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Make analysis the homepage
    path('', include('analyzer.urls')),

    # Optional: keep /analysis/ also working
    path('analysis/', include('analyzer.urls')),
]
