from django.views import generic
from .models import Post
from .forms import PostForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/post_list.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        form.fields['content'].widget.attrs['maxlength'] = 120
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.slug = post.title
            post.published_date = timezone.now()
            if request.user.is_authenticated:
                post.author = request.user
            else:
                post.author = get_object_or_404(User, pk=1)
            post.save()
            #messages.add_message(request, messages.SUCCESS, 'Merci pour votre message !')
            send_mail(post.title,post.content,'contact@yarig.com',['dsjclp@gmail.com'],)
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

