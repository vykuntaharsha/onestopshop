from django.contrib import admin
from .models import MarketingPreference

# Register your models here.


class MarketingPreferenceAdmin(admin.ModelAdmin):
    readonly_fields = ['mailchimp_msg','mailchimp_subscribed', 'timestamp', 'updatedAt']
    list_display = ['__str__', 'subscribed', 'updatedAt']
    class Meta:
        model = MarketingPreference
        fields = ['user', 'subscribed', 'mailchimp_msg', 'mailchimp_subscribed', 'timestamp', 'updatedAt']


admin.site.register(MarketingPreference, MarketingPreferenceAdmin)
