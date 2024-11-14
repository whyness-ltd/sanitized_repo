#----------------------------------------------------------------------
# Whyness Timesheet models
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.db import models

# Create your models here.
import logging
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

class Timeentry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    date = models.DateField(default=timezone.now)
    annual_leave = models.DecimalField('Annual leave', max_digits=4, decimal_places=2, default=0)
    statutory_holiday = models.DecimalField('Bank holiday', max_digits=4, decimal_places=2, default=0)
    sick_leave = models.DecimalField('Sick leave', max_digits=4, decimal_places=2, default=0)
    hr_recruitment = models.DecimalField('Recruitment', max_digits=4, decimal_places=2, default=0)
    sustainability = models.DecimalField('Sustainability - do not use', max_digits=4, decimal_places=2, default=0)
    design_architecture = models.DecimalField('Solution Design and Development', max_digits=4, decimal_places=2, default=0)
    functional = models.DecimalField('Functional - do not use', max_digits=4, decimal_places=2, default=0)
    admin_pmo = models.DecimalField('Admin PMO Financial - do not use', max_digits=4, decimal_places=2, default=0)
    comms_marketing = models.DecimalField('Market / Customer Research & Engagement, & Strategy', max_digits=4, decimal_places=2, default=0)
    product_development = models.DecimalField('Product development (tech) - do not use', max_digits=4, decimal_places=2, default=0)
    strategy = models.DecimalField('Business strategy - do not use', max_digits=4, decimal_places=2, default=0)
    user_research = models.DecimalField('User research and testing', max_digits=4, decimal_places=2, default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name = 'timeentry_update_user'
    )

    def total(self):
        ret = '{}'.format(self.annual_leave
            + self.statutory_holiday
            + self.sick_leave
            + self.hr_recruitment
            + self.sustainability
            + self.design_architecture
            + self.functional
            + self.admin_pmo
            + self.comms_marketing
            + self.product_development
            + self.strategy
            + self.user_research)
        return ret
    def __str__(self):
        msg = '{}: {} - {}'.format(self.user, self.date,
            (self.annual_leave
            + self.statutory_holiday
            + self.sick_leave
            + self.hr_recruitment
            + self.sustainability
            + self.design_architecture
            + self.functional
            + self.admin_pmo
            + self.comms_marketing
            + self.product_development
            + self.strategy
            + self.user_research)
        )
        return msg
    class Meta:
        verbose_name = "Timesheet entry"
        verbose_name_plural = "Timesheet entries"
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_user_date'),
        ]

