from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from guestbook import api, views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("stats", views.stats, name="stats"),
    path("stats/chart.png", views.chart_image, name="chart"),
    path("api/entries/", api.EntryListCreateApi.as_view(), name="api-entries"),
    path("api/entries/<int:id>/", api.EntryDeleteApi.as_view(), name="api-entry-delete"),
    path("api/stats/", api.StatsApi.as_view(), name="api-stats"),
    path("api/stats/chart/", api.ChartApi.as_view(), name="api-chart"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

handler400 = "common.errors.error_400"
handler403 = "common.errors.error_403"
handler404 = "common.errors.error_404"
handler500 = "common.errors.error_500"
