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

    def __str__(self):
        return f'{self.title} {self.desc}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'