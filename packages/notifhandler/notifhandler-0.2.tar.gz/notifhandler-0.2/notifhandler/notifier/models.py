# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models


class ListURL(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    ip_add = models.CharField(max_length=30)
    notif_type = models.CharField(max_length=200, null=True)
    data = models.TextField()
