from django.urls import path

from management_panel.views import ManagementPanelView

urlpatterns = [path("", ManagementPanelView.as_view(), name="management-view")]
