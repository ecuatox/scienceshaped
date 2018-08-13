from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView
from django.views.generic.base import ContextMixin
from scienceshaped import admin_history

from .models import Illustration, Testimonial
from files.models import Image
from tags.models import Tag


class IllustrationEdit(UpdateView, ContextMixin):
    model = Illustration
    fields = '__all__'

    template_name = 'projects/illustration_edit.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(IllustrationEdit, self).get_context_data(**kwargs)
        context.update({
            'illustration_tags': Tag.objects.filter(group__title='illustrations'),
            'images': Image.objects.all(),
            'new': self.kwargs['illustration_id'] is '0',

        })
        return context

    def get_object(self, queryset=None):
        try:
            return Illustration.objects.get(pk=self.kwargs['illustration_id'])
        except Illustration.DoesNotExist:
            return None

    def form_valid(self, form):
        response = super(IllustrationEdit, self).form_valid(form)
        if self.get_object():
            admin_history.log_change(self.request, self.object, form.cleaned_data['title'])
        else:
            admin_history.log_addition(self.request, self.object, form.cleaned_data['title'])
        return response


class TestimonialEdit(UpdateView, ContextMixin):
    model = Testimonial
    fields = '__all__'

    template_name = 'projects/testimonial_edit.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(TestimonialEdit, self).get_context_data(**kwargs)
        context.update({
            'images': Image.objects.all(),
            'new': self.kwargs['testimonial_id'] is '0',
        })
        return context

    def get_object(self, queryset=None):
        try:
            return Testimonial.objects.get(pk=self.kwargs['testimonial_id'])
        except Testimonial.DoesNotExist:
            return None

    def form_valid(self, form):
        response = super(TestimonialEdit, self).form_valid(form)
        if self.get_object():
            admin_history.log_change(self.request, self.object, form.cleaned_data['person'])
        else:
            admin_history.log_addition(self.request, self.object, form.cleaned_data['person'])
        return response


@permission_required('projects.delete_illustration')
def illustrationDelete(request, illustration_id):
    try:
        illustration = Illustration.objects.get(pk=illustration_id)
        illustration.delete()
        admin_history.log_deletion(request, illustration, illustration.title)
    except Illustration.DoesNotExist:
        pass

    return HttpResponseRedirect('/#illustrations')


@permission_required('projects.delete_testimonial')
def testimonialDelete(request, testimonial_id):
    try:
        testimonial = Testimonial.objects.get(pk=testimonial_id)
        testimonial.delete()
        admin_history.log_deletion(request, testimonial, testimonial.person)
    except Testimonial.DoesNotExist:
        pass

    return HttpResponseRedirect('/#testimonials')
