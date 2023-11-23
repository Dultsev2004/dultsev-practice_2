from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic
from .models import Application
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .forms import RegistrationUserForm, ApplicationForm, CategoryCreateForm

def index(request):
    applications = Application.objects.filter(state ='completed').order_by('-date')[:4]
    applications_count = Application.objects.filter(state ='progress').count()
    context = {'application_list': applications, 'applications_count': applications_count}

    return render(
        request, 'index.html', context
    )


class ProfileView(ListView, LoginRequiredMixin):
    template_name = 'portal/profile.html'
    context_object_name = 'application_list'

    def get_queryset(self):
        return Application.objects.filter(owner=self.request.user)

class ApplicationListView(generic.ListView):
    model = Application

class ApplicationCreateView(generic.CreateView):
    model = Application
    template_name = 'portal/application_form.html'
    form_class = ApplicationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class LoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('profile')


class LogoutView(LogoutView):
    template_name = 'index.html'


class RegistrationView(CreateView):
    form_class = RegistrationUserForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('index')


@login_required
def application_delete(request, pk):
    application = Application.objects.get(id=pk)
    if application.state == 'new':
        return render(request, 'applications_delete_confirm.html', {'application': application})

@login_required
def application_delete_confirm(request, pk):
    application = Application.objects.get(id=pk)
    application.delete()
    return redirect('profile')


@login_required
def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'categories.html', context)


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryCreateForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('categories')
    else:
        form = CategoryCreateForm()
    return render(request, 'category_create.html', {'form': form})


@login_required
def category_delete(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('categories')
