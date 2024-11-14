#----------------------------------------------------------------------
# Whyness prospects admin
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import logging
from django.contrib import admin
from django.contrib import messages

from whyness_prospect.models import Prospect

logger = logging.getLogger(__name__)


class ProspectAdmin(admin.ModelAdmin):
    model = Prospect
    fields = (
        'name',
        'email',
        'status',
        ('update_date', 'update_user', 'create_date'),
    )

    readonly_fields = [
        'update_user', 'update_date', 'create_date']
    search_fields = ['name', 'email']
    list_display = [
        'id',
        'name',
        'email',
        'status',
    ]

admin.site.register(Prospect, ProspectAdmin)
