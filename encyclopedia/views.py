from django import http
from django.conf.urls import url
from django.core.files import utils
from django.forms import fields
from django.forms.widgets import Textarea
from django.http import request
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django import urls
from django.urls import reverse
from random import randint

from . import util
import markdown

class NewEntryForm(forms.Form):
    new_entry_title = forms.CharField(label="Назва статті")
    new_entry_content = forms.CharField(widget=forms.Textarea, label="Текст статті")

def index(request):
    """Відображення всього списку статей на головній сторінці"""

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """Перехід на сторінку за шляхом wiki/НазваСтатті"""

    try:
        page_content = util.get_entry(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "page_content": markdown.markdown(page_content)
        })
    except AttributeError:
        return render(request, "encyclopedia/PageNotFound.html", {
            "title": title,
        })


def search(request):
    """Пошук за назвою статті"""

    query = request.GET.get('q')
    entries = util.list_entries()
    results = []
    for i in range(len(entries)):
        if query.upper() == entries[i].upper():
            return HttpResponseRedirect(f"{entries[i]}")
        elif query.upper() in entries[i].upper():
            results.append(entries[i])
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })

def create(request):
    """Створити нову статтю"""
    return render(request, "encyclopedia/CreateEntry.html",{
        "title_form": NewEntryForm(),
        
    })

def submit(request):
    """Публікувати статтю"""
    form = NewEntryForm(request.POST)
    if form.is_valid:
        entries = util.list_entries()
        title = request.POST.get("new_entry_title")
        content = request.POST.get("new_entry_content")
        if title in entries:
            return render(request, "encyclopedia/EntryExists.html",{
                "title": title
            })
        util.save_entry(title, content)
    return HttpResponseRedirect(reverse("index"))

def edit(request, title):
    """Редагування статті"""
    page_content = util.get_entry(title)
    parameters = {"new_entry_title": title, "new_entry_content": page_content}  # Шаблон для форми
    form = NewEntryForm(parameters)
    return render(request, "encyclopedia/EditEntry.html",{
        "form": form
    })

def save(request):
    """Публікувати статтю"""
    form = NewEntryForm(request.POST)
    if form.is_valid:
        entries = util.list_entries()
        title = request.POST.get("new_entry_title")
        content = request.POST.get("new_entry_content")
        util.save_entry(title, content)
    return HttpResponseRedirect(reverse("index"))

def random(request):
    """Перейти до випадкової статті"""
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries) - 1)]
    random_content = util.get_entry(random_title)
    return render(request, "encyclopedia/entry.html", {
        "title": random_title,
        "page_content": markdown.markdown(random_content)
    })

def redirect(request): 
    return HttpResponseRedirect(reverse('index'))