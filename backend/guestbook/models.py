from django.db import models


class Entry(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.id}: {self.name}"
