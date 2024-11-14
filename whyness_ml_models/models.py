#----------------------------------------------------------------------
# Whyness Machine Learning models
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
from django.db import models

class MBTI(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('whyness_django.AuthUser', on_delete=models.CASCADE)
    IE = models.CharField(max_length=1, default='')
    NS = models.CharField(max_length=1, default='')
    TF = models.CharField(max_length=1, default='')
    PJ = models.CharField(max_length=1, default='')
    update_ip = models.GenericIPAddressField(default='::1')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}: {}:{}:{}:{}".format(
            self.id,
            self.user,
            self.IE,
            self.NS,
            self.TF,
            self.PJ
        )
        return ret
