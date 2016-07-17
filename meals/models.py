from django.db import models

from accounts.models import User


class BaseMealElement(models.Model):
    name = models.CharField(max_length='32', unique=True)

    class Meta:
        abstract = True


class Rice(BaseMealElement):
    def __init__(self, *args, **kwargs):
        """
        [-1:]밥
        [-3:]라이스
        """
        super(Rice, self).__init__(*args, **kwargs)
        Rice._meta.get_field('name').help_text = '밥'


class Soup(BaseMealElement):
    def __init__(self, *args, **kwargs):
        """
        [-1:]국,탕
        [-2:]스프, 찌개
        """
        super(Soup, self).__init__(*args, **kwargs)
        Soup._meta.get_field('name').help_text = '국'


class Kimchi(BaseMealElement):
    def __init__(self, *args, **kwargs):
        """
        [-2:]김치, (깍)두기,(오이소)박이
        """
        super(Kimchi, self).__init__(*args, **kwargs)
        Kimchi._meta.get_field('name').help_text = '김치'


class Vegetable(BaseMealElement):
    def __init__(self, *args, **kwargs):
        super(Vegetable, self).__init__(*args, **kwargs)
        Vegetable._meta.get_field('name').help_text = '야채/채소'


class Dessert(BaseMealElement):
    def __init__(self, *args, **kwargs):
        super(Dessert, self).__init__(*args, **kwargs)
        Dessert._meta.get_field('name').help_text = '디저트'


class Source(BaseMealElement):
    def __init__(self, *args, **kwargs):
        super(Source, self).__init__(*args, **kwargs)
        Source._meta.get_field('name').help_text = '소스'


class UnknownMeal(BaseMealElement):
    def __init__(self, *args, **kwargs):
        super(UnknownMeal, self).__init__(*args, **kwargs)
        UnknownMeal._meta.get_field('name').help_text('기타 반찬')


class Meal(models.Model):
    class Type:
        LUNCH = 0
        DINNER = 1

    type = models.IntegerField(choices=Type, help_text='중식/석식')
    content = models.TextField(blank=False, default='급식이 제공되지 않습니다.', help_text='급식 내용')

    rice = models.ForeignKey(Rice, related_name='meals')
    soup = models.ForeignKey(Soup, related_name='meals')
    kimchi = models.ForeignKey(Kimchi, related_name='meals')
    vegetable = models.ForeignKey(Vegetable, related_name='meals')
    dessert = models.ForeignKey(Dessert, related_name='meals')
    source = models.ForeignKey(Source, related_name='meals')

    etc1 = models.ForeignKey(UnknownMeal, related_name='meals')
    etc2 = models.ForeignKey(UnknownMeal, related_name='meals')

    date = models.DateField(help_text='날짜')
    rate_avg = models.FloatField(default=0)

    def __str__(self):
        return "{} {} {}".format("중식" if self.type == 0 else "석식", self.date, self.content)


class Review(models.Model):
    writer = models.ForeignKey(User, help_text='작성자')
    meal = models.ForeignKey(Meal, help_text='급식')
    rate = models.FloatField(default=0.0, help_text='평점')
    content = models.TextField(blank=False, help_text='후기')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {} {}".format(self.meal, self.writer, self.rate)
