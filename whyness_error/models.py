#----------------------------------------------------------------------
# Whyness error models
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""
"""
from django.db import models

class ErrorLog(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    hostip = models.GenericIPAddressField(null=True)
    useragent = models.ForeignKey("whyness_django.UserAgent", on_delete=models.PROTECT)
    errorcode = models.TextField('Error code', blank=True)
    errormessage = models.TextField('Error message', blank=True)

    def __str__(self):
        ret = '{}: {}: {}'.format(
            self.create_date,
            self.errorcode,
            self.errormessage,
        )
        return ret
