from django.shortcuts import render, redirect, HttpResponse
from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from django.views.generic import UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from .utils import MailChimp
from .mixins import CsrfExemptMixin

MAILCHIMP_EMAIL_LIST_ID = getattr(settings,"MAILCHIMP_EMAIL_LIST_ID", None)


class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_url = '/settings/email/'
    success_message = 'your email preferences are updated. Thank you!'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated():
            return redirect('/account/login/?next=/settings/email/')
        return super(MarketingPreferenceUpdateView, self).dispatch(request)

    def get_context_data(self, **kwargs):
        context = super(MarketingPreferenceUpdateView,self).get_context_data()
        context['title'] = 'Update email preferences'
        return context

    def get_object(self, queryset=None):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj


class MailChimpWebhookView(CsrfExemptMixin, View):

    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')

        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            email = data.get('data[email]')
            response_status, response = MailChimp.check_subscription_status(email=email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == 'subscribed':
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == 'unsubscribed':
                is_subbed, mailchimp_subbed = (False, False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchimp_subbed, mailchimp_msg=str(data))
        return HttpResponse('Thank you!', status=200)
