from django.db import models


MAX_PADAWAN = 3


class Planets(models.Model):
    """Модель планет"""
    name = models.CharField(max_length=64, verbose_name='Наименование планеты')

    class Meta:
        db_table = 'planets'
        verbose_name = 'Планета'
        verbose_name_plural = 'Планеты'

    def __str__(self):
        return self.name


class Jedies(models.Model):
    """Модель джедаев"""
    name = models.CharField(max_length=64, verbose_name='Имя джедая')
    planet = models.ForeignKey(Planets)

    class Meta:
        db_table = 'jedies'
        verbose_name = 'Джедай'
        verbose_name_plural = 'Джедаи'

    def __str__(self):
        return f'{self.name} с планеты {self.planet.name}'

    @property
    def numbers_of_padawan(self):
        """"Кол-во падаванов"""
        return self.candidates_set.count()

    @property
    def can_take_padawan(self):
        """Может ли брать падаванов на обучение"""
        return self.numbers_of_padawan < MAX_PADAWAN


class Candidates(models.Model):
    """Модель кандидатов"""
    name = models.CharField(max_length=64, verbose_name='Имя кандидата')
    planet = models.ForeignKey(Planets, verbose_name='Планета')
    age = models.IntegerField(verbose_name='Возраст')
    email = models.EmailField(verbose_name='email')
    mentor = models.ForeignKey(Jedies, null=True, verbose_name='Наставник')
    is_padawan = models.BooleanField(
        default=False, verbose_name='Яаляется падаваном')
    answers = models.TextField(
        default='[]', verbose_name='Тестовые вопросы и ответы кандидата')

    class Meta:
        db_table = 'candidates'
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

    def __str__(self):
        return f'{self.name} с планеты {self.planet.name}'


class Questions(models.Model):
    """Вопросы тестового задания"""
    question = models.TextField(max_length=128)

    class Meta:
        db_table = 'questions'
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question


class Quests(models.Model):
    """Задания"""
    order_code = models.CharField(max_length=16)
    questions = models.ManyToManyField(Questions)

    class Meta:
        db_table = 'quests'
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.order_code
