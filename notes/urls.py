from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import register, login, logout, user_profile,TaskViewSet, update_profile, update_profile_photo, SubjectViewSet, UnitViewSet

# Initialize the DefaultRouter
router = DefaultRouter()
# Register the viewsets with the router
router.register(r'subjects', SubjectViewSet)
router.register(r'units', UnitViewSet)
router.register(r'tasks', TaskViewSet, basename='task')


urlpatterns = [
    # Register the user-related paths
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('users/<int:id>/', user_profile, name='user_profile'),
    
    # Include the router URLs for subjects and units
    path('', include(router.urls)),

    # Additional user-related paths
    path('subjects/<int:pk>/units/', UnitViewSet.as_view({'get': 'units_by_subject'}), name='subject-units'),
    path('users/<int:id>/update/', update_profile, name='update_profile'),
    path('users/<int:id>/update-profile-photo/', update_profile_photo, name='update_profile_photo'),  # For updating profile photo
]

