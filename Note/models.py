from django.db import models

class Tag(models.Model):
    name = models.CharField(
        max_length=30, 
        unique=True,
        verbose_name="Название тега"
    )
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
    

class Note(models.Model):
    title = models.CharField(
        max_length=100, 
        verbose_name="Заголовок заметки"
    )

    text = models.TextField(
        verbose_name="Текст заметки"
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="notes",
        blank=True,
        verbose_name="Теги"
    )

    created_ad = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
 
