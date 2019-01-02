from django.conf.urls import url
from . import views

app_name = 'new_beam'

urlpatterns = [
    url(r'^$', views.new_beam, name='new_beam'),
    url(r'^new_beam/(?P<beam_id>\d+)$', views.beam_diagram, name='beam_diagram'),
    url(r'^new_beam/solve/(?P<beam_id>\d+)$', views.beam_diagram_solve, name='beam_diagram_solve'),
]
