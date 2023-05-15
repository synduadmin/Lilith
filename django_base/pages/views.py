# pages/views.py
from django.views.generic.edit import FormView
from leads.forms import LeadForm
from django.urls import reverse_lazy

class HomePageView(FormView):
    template_name = 'home.html'
    form_class = LeadForm
    success_url = reverse_lazy('leads:thank_you')  # redirects to thank you page after form submission

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        form.save()  # save the form data to database
        return super().form_valid(form)
