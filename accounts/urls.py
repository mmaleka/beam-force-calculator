from django.conf.urls import url
from . import views
from django.urls import include
from django.contrib.auth import views as auth_views



app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^register_view/$', views.register_view, name='register_view'),
    url(r'^logout/$', views.logout_view, name="logout_view"),
    url(r'^profile_view/$', views.profile_view, name="profile_view"),
    url(r'password_change/$',auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html',success_url='/accounts/password_change_done')),
    url(r'password_change_done/',auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html')),
    url(r'password_reset/$',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',email_template_name='registration/password_reset_email.html',subject_template_name='registration/password_reset_email.txt',success_url='/accounts/password_reset_done/',from_email='mpho.maleka3@gmail.com'), name='password_reset'),
    url(r'password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html')),
    url(r'password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',success_url='/accounts/password_reset_complete/'), name='password_reset_confirm'),
    url(r'password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html')),
]
