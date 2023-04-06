from django.db import models

class zdna(models.Model):
    md5pass = models.CharField(max_length=100, default="")
    md5data = models.CharField(max_length=100, default="")
    randnum = models.CharField(max_length=100, default="")
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_time']

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     if update_fields is not None and "name" in update_fields:
    #         update_fields = {"slug"}.union(update_fields)
    #     super().save(
    #         force_insert=force_insert,
    #         force_update=force_update,
    #         using=using,
    #         update_fields=update_fields,
    #     )


