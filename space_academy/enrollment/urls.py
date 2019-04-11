from django.conf.urls import url

urlpatterns = [
    # Главная страница
    url(r'^$', 'enrollment.views.main_page'),
    # Завершение ответов на вопросы
    url(r'^end_quest/(?P<candidate_id>\d+)/$', 'enrollment.views.end_quest'),
    # Регистрация нового кандидата
    url(r'^register/$', 'enrollment.views.new_candidate'),
    # Вопросы для нового кандидата
    url(r'^register_quest/$', 'enrollment.views.new_candidate_quest'),
    # Отображение всех джедаев
    url(r'^jedies/$', 'enrollment.views.all_jedies'),
    # Отображение кандидатов для конкретного Джедая
    url(r'^jedies/(?P<jedi_id>\d+)/$', 'enrollment.views.all_candidates'),
    # Отображение ответов конкретного кандидата для конкретного Джедая
    url(r'^jedies/(?P<jedi_id>\d+)/(?P<candidate_id>\d+)/answers/$',
        'enrollment.views.answers_candidate'),
]
