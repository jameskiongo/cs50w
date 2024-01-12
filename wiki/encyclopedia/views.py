import random

import markdown
from django import forms
from django.shortcuts import render

from . import util


def convert_md(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries()},
    )


def wiki(request, title):
    html_content = convert_md(title)
    if html_content == None:
        return render(
            request, "encyclopedia/error.html", {"message": "Content Not Found"}
        )
    else:
        return render(
            request,
            "encyclopedia/entry_page.html",
            {
                "title": title,
                "content": html_content,
            },
        )


def search(request):
    if request.method == "POST":
        search_request = request.POST["q"]
        html_content = convert_md(search_request)
        if html_content is not None:
            return render(
                request,
                "encyclopedia/entry_page.html",
                {"title": search_request, "content": html_content},
            )
        else:
            return render(
                request, "encyclopedia/error.html", {"message": "content not found"}
            )


def new_page(request):
    return render(request, "encyclopedia/new_page.html")


def save_content(request):
    if request.method == "POST":
        content = request.POST["content"]
        title = request.POST["title"].lower()
        check_title = util.list_entries()
        lowercase_list = [item.lower() for item in check_title]
        if title in lowercase_list:
            return render(
                request,
                "encyclopedia/error.html",
                {"message": "content already exists"},
            )
    util.save_entry(title, content)
    return render(
        request,
        "encyclopedia/entry_page.html",
        {"title": title, "content": content},
    )


def edit_content(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(
            request,
            "encyclopedia/edit_page.html",
            {
                "title": title,
                "content": content,
            },
        )


def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        html_content = convert_md(title)
        return render(
            request,
            "encyclopedia/entry_page.html",
            {
                "title": title,
                "content": html_content,
            },
        )


def random_page(request):
    pages = util.list_entries()
    random_title = random.choice(pages)
    content = convert_md(random_title)
    return render(
        request,
        "encyclopedia/entry_page.html",
        {
            "title": random_title,
            "content": content,
        },
    )
