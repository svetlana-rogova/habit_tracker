from rest_framework.routers import DefaultRouter

from tracker.views import HabitViewSet

app_name = 'tracker'

router = DefaultRouter()
router.register(r'habit', HabitViewSet, basename='habit')

urlpatterns = router.urls
