# pages/views.py
from django.views.generic.edit import FormView
from leads.forms import LeadForm

class HomePageView(FormView):
    template_name = 'home.html'
    form_class = LeadForm
    success_url = '/thank-you/'

    def form_valid(self, form):
        # capture the user's IP
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')

        # store the IP in the form and save it
        form.instance.ip_address = ip
        form.save()

        return super().form_valid(form)
