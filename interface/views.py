from django.shortcuts import render, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


# Create your views here.
class Index(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name, context={})


# LoginRequiredMixin
class Home(LoginRequiredMixin, View):
    template_name = 'account_dashboard.html'

    def get(self, request):
        return render(request, self.template_name, context={})
