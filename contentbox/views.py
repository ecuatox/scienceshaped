from django.views.generic import UpdateView

from .models import ContentBox


class ContentBoxEdit(UpdateView):
    model = ContentBox
    fields = ['title', 'content', 'light']

    template_name = 'contentbox/contentbox.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return ContentBox.get(self.kwargs['title'])

    # def form_valid(self, form):
    #     messages.success(self.request, 'Content of "%s" was successfully saved' % form.cleaned_data['title'])
    #     return super(ContentBoxEdit, self).form_valid(form)
