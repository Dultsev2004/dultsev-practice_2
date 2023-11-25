from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic
from .models import Application, Category
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .forms import RegistrationUserForm, ApplicationForm, CategoryCreateForm, ApplicationDoneForm, ApplicationInWorkForm


def index(request):
    applications = Application.objects.filter(state='completed').order_by('-date')[:4]
    applications_count = Application.objects.filter(state='progress').count()
    context = {'application_list': applications, 'applications_count': applications_count}

    return render(
        request, 'index.html', context
    )


class ProfileView(ListView, LoginRequiredMixin):
    template_name = 'portal/profile.html'
    context_object_name = 'application_list'

    def get_queryset(self):
        return Application.objects.filter(owner=self.request.user)


class ProfileFilter(ListView, LoginRequiredMixin):
    context_object_name = 'applications_list'
    template_name = 'portal/profile.html'
    def get_queryset(self):
        return Application.objects.filter(owner=self.request.user, state=self.request.GET.get('state')[0])


class ApplicationListView(ListView, LoginRequiredMixin):
    model = Application
    context_object_name = 'application_list'
    template_name = 'portal/application_list.html'

    def get_queryset(self):
        current_state = self.request.GET.get('state', 'all')
        if current_state == 'all':
            return Application.objects.filter(owner=self.request.user)
        else:
            return Application.objects.filter(owner=self.request.user, state=current_state)


class ApplicationCreateView(generic.CreateView):
    model = Application
    template_name = 'portal/application_form.html'
    form_class = ApplicationForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()

        return redirect('profile')


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
        return render(request, 'portal/application_delete_confirm.html', {'application': application})


class ApplicationDelete(DeleteView):
    model = Application
    template_name = 'portal/applications_delete_confirm.html'
    success_url = reverse_lazy('index')


@login_required
def category_list(request):
    categories_list = Category.objects.all()
    return render(request, 'portal/category_list.html', {'categories_list': categories_list})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryCreateForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('category_list')
    else:
        form = CategoryCreateForm()
    return render(request, 'portal/category_create.html', {'form': form})


@login_required
def category_delete(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('category_list')


class ApplicationUpdateStatusDoneView(UpdateView, LoginRequiredMixin):
    model = Application
    form_class = ApplicationDoneForm
    context_object_name = 'application'
    template_name = 'portal/application_update_status_done.html'

    def get_queryset(self):
        return Application.objects.filter(state='new')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.state = 'completed'
        instance.save()

        return redirect('application_list')


class ApplicationUpdateStatusInWorkView(ApplicationUpdateStatusDoneView):
    form_class = ApplicationInWorkForm
    template_name = 'portal/application_update_status_inwork.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.state = 'progress'
        instance.save()

        return redirect('application_list')

