from django.urls import path
from . import views, AdminViews, HodViews, SupervisorViews, StaffViews

urlpatterns = [
    path('', views.doLogin, name='login'),
    path('logout/', views.doLogout, name="logout"),
    path('change_password/', views.change_password, name='change_password'),
    
    path('admin_dashboard/', AdminViews.admin_dashboard, name='admin'),
    path('staff_list/', AdminViews.staff_list, name='staff_list'),
    path('add_staff/', AdminViews.add_staff_info, name='add_staff_info'),
    path('update_staff/<int:user_id>/', AdminViews.update_staff_info, name='update_staff_info'),
    path('get-units-by-department/', AdminViews.get_units_by_department, name='get_units_by_dept'),
    path('staff_list/download/', AdminViews.download_staff_data, name='download_staff_data'),
    path('download_appraisal/', AdminViews.download_appraisal_data, name='download_appraisal_data'),
    path('admin_results/', AdminViews.admin_view_results, name='admin_view_results'),
    path('admin_view/<int:appraisal_id>/', AdminViews.admin_view, name='admin_view'),

    path('hod_dashboard/', HodViews.hod_dashboard, name='hod'),
    path('hod_form/', HodViews.hod_form, name='hod_form'),
    path('hod_view_appraisals/', HodViews.hod_view_appraisals, name='hod_view_appraisals'),
    path('hod_result/', HodViews.hod_result, name='hod_result'),
    path('staff_hod_review/<int:appraisal_id>/', HodViews.staff_hod_review, name='staff_hod_review'),
    path('staff_hod_view/<int:appraisal_id>/', HodViews.staff_hod_view, name='staff_hod_view'),
    path('staff_hod_rating/<int:appraisal_id>/', HodViews.staff_hod_rating, name='staff_hod_rating'),

    path('supervisor_hod_review/<int:appraisal_id>/', HodViews.supervisor_hod_review, name='supervisor_hod_review'),
    path('supervisor_hod_view/<int:appraisal_id>/', HodViews.supervisor_hod_view, name='supervisor_hod_view'),
    path('supervisor_hod_rating/<int:appraisal_id>/', HodViews.supervisor_hod_rating, name='supervisor_hod_rating'),

    path('supervisor_dashboard/', SupervisorViews.supervisor_dashboard, name='supervisor'),
    path('supervisor_form/', SupervisorViews.supervisor_form, name='supervisor_form'),
    path('supervisor_view_appraisals/', SupervisorViews.supervisor_view_appraisals, name='supervisor_view_appraisals'),
    path('supervisor_result/', SupervisorViews.supervisor_result, name='supervisor_result'),
    path('supervisor_review/<int:appraisal_id>/', SupervisorViews.supervisor_review, name='supervisor_review'),
    path('supervisor_view/<int:appraisal_id>/', SupervisorViews.supervisor_view, name='supervisor_view'),
    path('supervisor_rating/<int:appraisal_id>/', SupervisorViews.supervisor_rating, name='supervisor_rating'),
    path('supervisor_initiate/', SupervisorViews.supervisor_initiate_appraisal, name='supervisor_initiate_appraisal'),

    path('staff_dashboard/', StaffViews.staff_dashboard, name='staff'),
    path('staff_form/', StaffViews.staff_form, name='staff_form'),
    path('staff_view_appraisal/', StaffViews.staff_view_appraisal, name='staff_view_appraisal'),
    path('staff_result/', StaffViews.staff_result, name='staff_result'),
    path('staff_review/<int:appraisal_id>/', StaffViews.staff_review, name='staff_review'),
    path('staff_initiate/', StaffViews.staff_initiate_appraisal, name='staff_initiate_appraisal'),
    
]