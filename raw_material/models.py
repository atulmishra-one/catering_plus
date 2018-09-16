from django.db import models
from account.models import CaterUser

# Create your models here.


class RawMaterial(models.Model):
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sender = models.ForeignKey(CaterUser, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_send = models.DateTimeField(default=None)
    updated = models.DateTimeField(auto_now_add=True)

    PENDING = 0
    DONE = 1
    STATUS = (
        (PENDING, 'Pending'),
        (DONE, 'Done')
    )
    status = models.SmallIntegerField(choices=STATUS, default=PENDING)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Raw Material Request'







