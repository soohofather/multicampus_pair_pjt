from django.shortcuts import render, redirect
from .models import Review

# Create your views here.


def index(request):

    reviews = Review.objects.all()
    context = {
        "reviews": reviews,
    }

    return render(request, "app_pairpjt1/index.html", context)


def review(request):

    return render(request, "app_pairpjt1/review.html")


def create(request):

    title = request.GET.get("title")
    content = request.GET.get("content")
    created_at = request.GET.get("created_at")

    Review.objects.create(title=title, content=content)

    return redirect("pjt1:index")


def detail(request, pk):

    content = Review.objects.get(pk=pk)

    context = {
        "content": content,
    }

    return render(request, "app_pairpjt1/detail.html", context)


def delete(request, pk):

    delete = Review.objects.get(pk=pk)

    delete.delete()

    return redirect("pjt1:index")


def edit(request, pk):

    edit_content = Review.objects.get(pk=pk)

    context = {
        "edit_content": edit_content,
    }

    return render(request, "app_pairpjt1/edit.html", context)


def update(request, pk):

    old_content = Review.objects.get(pk=pk)

    old_content.title = request.GET.get("title")
    old_content.content = request.GET.get("content")

    old_content.save()

    return redirect("pjt1:index")
