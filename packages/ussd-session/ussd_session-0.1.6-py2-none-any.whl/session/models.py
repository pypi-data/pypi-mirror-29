# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Session(models.Model):
    phone_number = models.CharField(max_length=10)
    session_id = models.CharField(max_length=40)
    service_code = models.CharField(max_length=15)
    operator = models.CharField(max_length=10)
    initiation_message = models.CharField(max_length=15)
    succeeded = models.BooleanField(default=False)
    menu_option = models.PositiveSmallIntegerField(null=True)
    sequence_at_menu = models.PositiveSmallIntegerField(null=True)
    date_created = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=30, null=True)
    method = models.CharField(max_length=50, null=True)
    step_at_paged = models.PositiveSmallIntegerField(null=True)
    page_stop = models.PositiveSmallIntegerField(null=True)
    selector = models.PositiveSmallIntegerField(null=True)
    actor_first_name = models.CharField(max_length=20)
    actor_last_name = models.CharField(max_length=20)

    def __str__(self):
        return '%s - %s' % (self.phone_number, self.session_id)