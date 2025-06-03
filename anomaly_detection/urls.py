from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from model.views import LogEntryViewSet, AnomalyReportViewSet

router = DefaultRouter()
router.register(r'logs', LogEntryViewSet)
router.register(r'anomalies', AnomalyReportViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
