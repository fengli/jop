from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from jop.posts.forms import PostForm
from jop.posts.models import Post, CachedImage
from django.views.decorators.csrf import csrf_exempt
from voting.models import Vote


def post_list(request):
    posts = Post.objects.all()

    return render_to_response(
        'posts/post_list.html',
        {
            'posts': posts
        },
        context_instance=RequestContext(request))


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    return render_to_response(
        'posts/post_detail.html',
        {
            'post': post
        },
        context_instance=RequestContext(request))


@login_required
def new_post(request):
    post_form = PostForm(request.POST if 'submit' in request.POST else None)

    if request.method == 'POST':
        if post_form.is_valid():
            cd = post_form.cleaned_data
            cached_image = CachedImage()
            cached_image.image_url = cd['image_url']
            cached_image.save()

            post = Post()
            post.title = cd['title']
            post.description = cd['description']
            post.cached_image = cached_image
            post.update_date = datetime.now()
            post.author = request.user
            post.save()
            post.tags.add(*cd['tags'].split(','))

            return HttpResponseRedirect(
                reverse("posts:detail", kwargs={'slug': post.slug}))

    return render_to_response(
        'posts/post_new.html',
        {
            'post_form': post_form
        },
        context_instance=RequestContext(request))


@login_required
@csrf_exempt
def vote_up(request, slug):
    template_name = 'posts/includes/post_footer.html'

    if not request.method == 'POST':
        raise Http404

    post = get_object_or_404(Post, slug=slug)
    vote = Vote.objects.get_for_user(post, request.user)

    if vote:
        Vote.objects.record_vote(post, request.user, 0)
    else:
        Vote.objects.record_vote(post, request.user, 1)

    return render_to_response(
        template_name,
        {'post': post},
        context_instance=RequestContext(request))
