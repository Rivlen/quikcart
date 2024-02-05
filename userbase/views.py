from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from main.models import Category
from .forms import MemberRegistrationForm
from django.contrib.auth.models import Group


class MemberSignUpView(generic.CreateView):
    form_class = MemberRegistrationForm
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        members_group = Group.objects.get(name='Members')  # Make sure 'Members' group exists
        self.object.groups.add(members_group)
        return response

    def get_context_data(self, **kwargs):
        """
        Override the default context data to include the list of categories.
        """
        context = super().get_context_data(**kwargs)
        return context
