import json

from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render_to_response, redirect, render

from .forms import CandidateForm
from .models import Candidates, Jedies, Questions, Quests


def main_page(request):
    """Главная страница"""
    return render_to_response('main.html')


def all_jedies(request):
    """Отображение всех джедаев"""
    # Если есть фильтрация, то отфильтруем
    filter_name = Q()
    q = request.GET.get('q')
    if q:
        filter_name &= Q(name__icontains=q)
    params = {
        'jedies': Jedies.objects.filter(filter_name)
    }

    return render_to_response('jedies.html', params)


def all_candidates(request, jedi_id=None):
    """Отображение кандидатов для джедая"""
    # Получим джедая по id
    try:
        jedi = Jedies.objects.get(id=jedi_id)
        filter_name = Q()
        q = request.GET.get('q')
        # Если задана фильтрация, то добавим в фильтр
        if q:
            filter_name &= Q(name__icontains=q)
        params = {
            'candidates': Candidates.objects.filter(
                filter_name, planet_id=jedi.planet_id, is_padawan=False),
            'jedi': jedi
        }
        result = render_to_response('candidates.html', params)
    except Jedies.DoesNotExist:
        params = {'message': 'Не найден Джедай по указанным параметрам!'}
        result = render(request, 'error_page.html', params)

    return result


def new_candidate(request):
    """Запрос формы регистрации"""
    form = CandidateForm()
    params = {'form': form}

    return render(request, 'candidate.html', params)


def new_candidate_quest(request):
    """Новый кандидат"""
    # Получаем рег. форму кандидата
    form = CandidateForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        # Если форма валидная, то сохраним данные кандидата
        candidate = form.save()
        # Поскольку работа с орденами в постановке никак не описана, то будем
        # брать всегда первый, он же и единственный. Именно его вопросы и будут.
        quest = Quests.objects.first()
        if quest:
            questions = quest.questions.all()
            params = {
                'candidate': candidate,
                'questions': questions,
                'questions_ids': questions.values_list('id', flat=True)
            }
            result = render(request, 'candidate_quest.html', params)
        else:
            params = {'message': 'Задание ордена не найдено!'}
            result = render(request, 'error_page.html', params)
    else:
        result = redirect('/register')

    return result


def end_quest(request, candidate_id=None):
    """Завершение задания кандидата"""
    if request.method == 'POST':
        try:
            candidate = Candidates.objects.get(id=candidate_id)
            question_ids = request.POST.get('questions_ids', [])
            if question_ids:
                question_ids = list(map(int, question_ids[1:-1].split(',')))
            # Получим словарь вопросов
            questions = dict(
                Questions.objects.filter(
                    id__in=question_ids
                ).values_list('id', 'question')
            )
            # Заполним ответы кандидата с вопросами, чтобы знать, на что он 
            # отвечал, если вдруг вопросы изменятся или вовсе удалятся
            answers = []
            for question_id in question_ids:
                answer_key = f'answer_{question_id}'
                answers.append({'question': questions.get(question_id),
                                'answer': request.POST.get(answer_key)})
            # запишем ответы в кандидата и сохраним
            candidate.answers = json.dumps(answers)
            candidate.save()
            result = redirect('/')
        except Candidates.DoesNotExist:
            params = {'message': 'Возникла проблема при получении кандидата!'}
            result = render(request, 'error_page.html', params)
        # Сделаем из строки список id
    else:
        result = redirect('/')

    return result


def answers_candidate(request, candidate_id=None, jedi_id=None):
    """Отображение страницы ответов кандидатов"""
    # Получим джедая, который хочет рассмотреть падавана
    try:
        jedi = Jedies.objects.get(id=jedi_id)
        # Получим кандидата, по которому смотрим ответы
        candidate = Candidates.objects.get(id=candidate_id)
        # загрузим его ответы
        answers = json.loads(candidate.answers)
        # Приведем к списку кортежей, чтобы в шаблоне отобразить
        answers = [(i['question'], i['answer']) for i in answers]
        # Если пришел запрос методом POST, то это принятие кандидата
        if request.method == 'POST':
            # если джедай может брать падаванов
            if jedi.can_take_padawan:
                # то сделаем выбранного кандидата падаваном
                candidate.mentor_id = jedi_id
                candidate.is_padawan = True
                candidate.save()
                send_mail('Сообщение от Джедая',
                          f'Уважаемый {candidate.name}! Теперь Вы - Падаван!',
                          'starsorder@jedies.com',
                          [candidate.email], fail_silently=False)
                params = {
                    'candidates': Candidates.objects.filter(
                        planet=jedi.planet_id, is_padawan=False),
                    'jedi': jedi
                }
                result = render_to_response('candidates.html', params)
            else:
                params = {'message': 'Вы не можете принять больше кандидатов!'}
                result = render(request, 'error_page.html', params)
        # иначе просто показ ответов выбранного кандидата
        else:
            params = {
                'candidate': candidate,
                'jedi': jedi,
                'answers': answers
            }
            result = render(request, 'answers.html', params)
    except Jedies.DoesNotExist:
        params = {'message': 'Не найден Джедай по указанным параметрам!'}
        result = render(request, 'error_page.html', params)
    except Candidates.DoesNotExist:
        params = {'message': 'Не найден Кандидат по указанным параметрам!'}
        result = render(request, 'error_page.html', params)

    return result
