from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import register, login, logout, SubjectViewSet, UnitViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'units', UnitViewSet)

urlpatterns = [
    # User Registration and Login URLs
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),  # Add logout here

    # API endpoints for subjects and units
    path('', include(router.urls)),
    path('subjects/<int:pk>/units/', UnitViewSet.as_view({'get': 'units_by_subject'}), name='subject-units'),
]
