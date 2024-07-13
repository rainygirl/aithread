from django.db.models import QuerySet
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Feed


def index(request):
    return list_feed(request, "", 1)


def signup(request):
    return render(request, "signup.html")


def list_feed(request, forumid: str = "", page: int = 1):
    PER_PAGE: int = 15

    entries: QuerySet[Feed] = Feed.objects
    if forumid != "":
        entries = entries.filter(forumid=forumid)

    entries = entries.order_by("-id")

    p = Paginator(entries, per_page=PER_PAGE)
    feeds = p.get_page(page)
    paging: list[int] = p.page_range

    return render(
        request,
        "list.html",
        context={"feeds": feeds, "paging": paging, "feed_page": page},
    )


def view(request, forumid: str, feed_id: int):
    PER_PAGE: int = 15

    feed: Feed = Feed.objects.get(id=feed_id, forumid=forumid)

    feed_page: int = Feed.objects.filter(id__gt=feed_id).count() // PER_PAGE + 1

    entries: QuerySet[Feed] = Feed.objects.all().order_by("-id")

    p = Paginator(entries, per_page=PER_PAGE)
    feeds = p.get_page(feed_page)
    paging: list[int] = p.page_range

    return render(
        request,
        "view.html",
        context={
            "feed": feed,
            "feeds": feeds,
            "paging": paging,
            "feed_page": feed_page,
        },
    )
