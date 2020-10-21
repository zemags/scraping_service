from django.db import models

from scraping.utils import from_cyrrilic_to_eng


class City(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='City name',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        """Show correctly on admin page"""
        verbose_name = 'City name'
        verbose_name_plural = 'City\'s name'

    def __str__(self):
        # redefine name
        return self.name

    def save(self, *args, **kwargs):
        # redefine save to convert cyrillic to english
        if not self.slug:
            self.slug = from_cyrrilic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Programming Language',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        """Show correctly on admin page"""
        verbose_name = 'Programming Language'
        verbose_name_plural = 'Programming Languages'

    def __str__(self):
        # redefine name
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrrilic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Title')
    company = models.CharField(max_length=250, verbose_name='Company')
    description = models.TextField(verbose_name='Description')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='City')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Language')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancys'

    def __str__(self):
        return self.title

