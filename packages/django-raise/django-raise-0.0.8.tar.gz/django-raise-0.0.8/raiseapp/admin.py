from django.contrib import admin

from . import models


class PledgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'active', 'amount', 'created')
    list_filter = ('campaign', 'active')


admin.site.register([
    models.Campaign,
    models.Reward,
    models.Reminder,
])


admin.site.register(models.Pledge, PledgeAdmin)
