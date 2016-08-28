from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from jop.posts.forms import PostForm, MemeForm
from jop.posts.models import Post, CachedImage, Meme
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
    form = MemeForm()

    return render_to_response(
        'posts/post_detail.html',
        {
            'post': post,
            'form': form
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
            post.cached_image = cached_image
            post.update_date = datetime.now()
            post.author = request.user
            post.save()
            post.tags.add(*cd['tags'].split(','))
            meme = Meme()
            meme.meme = cd['title']
            meme.update_date = datetime.now()
            meme.author = request.user
            meme.post = post
            meme.save()

            post.best_meme = meme
            post.save()

            return HttpResponseRedirect(
                reverse("posts:detail", kwargs={'slug': post.slug}))

    return render_to_response(
        'posts/post_new.html',
        {
            'post_form': post_form
        },
        context_instance=RequestContext(request))


@login_required
def new_meme(request, slug):
    meme_form = MemeForm(request.POST if 'submit' in request.POST else None)

    if request.method == 'POST':
        if meme_form.is_valid():
            cd = meme_form.cleaned_data
            post = get_object_or_404(Post, slug=slug)
            meme = Meme()
            meme.meme = cd['meme']
            meme.update_date = datetime.now()
            meme.author = request.user
            meme.post = post
            meme.save()

            return HttpResponseRedirect(
                reverse("posts:detail", kwargs={'slug': post.slug}))

    raise Http404


@login_required
@csrf_exempt
def vote_up_meme(request, slug):
    template_name = 'posts/includes/meme_footer.html'

    if not request.method == 'POST':
        raise Http404

    meme = get_object_or_404(Meme, slug=slug)
    vote = Vote.objects.get_for_user(meme, request.user)

    if vote:
        Vote.objects.record_vote(meme, request.user, 0)
        meme.num_votes -= 1
        meme.post.num_votes -= 1
    else:
        Vote.objects.record_vote(meme, request.user, 1)
        meme.num_votes += 1
        meme.post.num_votes += 1
        if meme.num_votes > meme.post.current_best_votes:
            meme.post.current_best_votes += 1
            meme.post.best_meme = meme

    meme.save()
    meme.post.save()

    return render_to_response(
        template_name,
        {'meme': meme},
        context_instance=RequestContext(request))
