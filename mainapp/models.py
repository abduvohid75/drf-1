from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='название')
    preview = models.ImageField(verbose_name='изображение', null=True, blank=True)
    desc = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.title} {self.desc}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name='название')
    preview = models.ImageField(verbose_name='изображение', null=True, blank=True)
    desc = models.TextField(verbose_name='описание')
    link = models.URLField(verbose_name='ссылка на видео', null=True, blank=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', default=None, null=True,
                               blank=True)

    def __str__(self):
        return f'{self.title} {self.desc}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    user = models.CharField(max_length=100, verbose_name='пользователь')
    date = models.DateTimeField(verbose_name='время', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', default=None, null=True,
                               blank=True)
    sum_pay = models.IntegerField(verbose_name='сумма оплаты')
    pay_met = models.BooleanField(verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user} {self.course} {self.sum_pay} {self.pay_met}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'