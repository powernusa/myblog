from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail


def post_list(request):
    print("\n\n\n========== post_list called ==========\n")
    posts = Post.published.all()
    page = request.GET.get("page")
    print("* paginate page: ", page)
    paginator = Paginator(posts, 2)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    context = {
        "posts": post_list,
    }
    return render(request, "blog/post/list.html", context=context)


def post_detail(request, year, month, day, post):
    print("\n\n\n---------- post_detail called ----------\n")
    print("*DEBUG post_detail request: ", request)
    print("*DEBUG post_detail request.body: ", request.body)
    print("*DEBUG post_detail request.path: ", request.path)
    print("*DEBUG post_detail request.encoding: ", request.encoding)

    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False

    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(subject, message, cd["email"], [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()

    context = {
        "post": post,
        "form": form,
        "sent": sent,
    }
    return render(request, "blog/post/share.html", context=context)

