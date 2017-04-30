from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.http import JsonResponse

from django.views.generic import ListView, DetailView

from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import time

from .models import Book, Vote, Category, Author, ProfileCategory, ProfileAuthor, ProfileBook
import re

from django.db.models import Q

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
User = get_user_model()


class Index(ListView):
    model = Book
    paginate_by = 30
    template_name = 'SimpleBookStore/index.html'
    context_object_name = 'books'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            author_ids = ProfileAuthor.objects.filter(profile=profile, status=1).values_list('author_id', flat=True)
            category_ids = ProfileCategory.objects.filter(profile=profile, status=1).values_list('category_id', flat=True)

            return Book.objects.filter(Q(author__in=author_ids) | Q(category__in=category_ids)).select_related(
                'author', 'category'
            )
        else:
            return Book.objects.select_related(
                'author', 'category'
            )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['segment_title'] = 'New Books'
        return context


class CategoryView(ListView):
    model = Book
    paginate_by = 30
    template_name = 'SimpleBookStore/category.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.filter(category_id=self.kwargs.get('pk')).select_related(
            'author', 'category'
        )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['category'] = category = Category.objects.get(pk=self.kwargs.get('pk'))
        context['segment_title'] = category.title
        return context


class UserBooksView(ListView):
    model = Book
    paginate_by = 30
    template_name = 'SimpleBookStore/user_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        books_ids = ProfileBook.objects.filter(profile=self.request.user.profile,
                                               status=self.kwargs.get('status')).values_list('book_id', flat=True)

        return Book.objects.filter(id__in=books_ids).select_related(
            'author', 'category'
        )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['segment_title'] = "My Books"
        return context


class AuthorView(ListView):
    model = Book
    paginate_by = 30
    template_name = 'SimpleBookStore/author.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.filter(author_id=self.kwargs.get('pk')).select_related(
            'author', 'category'
        )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['author'] = author = Author.objects.get(pk=self.kwargs.get('pk'))
        context['segment_title'] = author.name
        return context


class SearchView(ListView):
    model = Book
    paginate_by = 30
    template_name = 'SimpleBookStore/search.html'
    context_object_name = 'books'

    def get_query(self):
        try:
            query = self.request.GET.get("query")
        except:
            query = ''
        return query

    def get_queryset(self):
        object_list = []
        if self.get_query() != '':
            object_list = Book.objects.filter(title__icontains=self.get_query())

        return object_list

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['segment_title'] = self.get_query()
        return context


class BookView(DetailView):
    model = Book
    template_name = 'SimpleBookStore/book.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['user_status'] = 0

        if self.request.user.is_authenticated:
            context['user_status'] = ProfileBook.objects.get(profile=self.request.user.profile,
                                                             book=self.get_object()).status
        return context


def book_action_view(request):
    time.sleep(1)
    if request.user.is_authenticated() and request.method == "POST":
        id = request.POST.get('id')
        action = request.POST.get('action')

        obj, created = ProfileBook.objects.update_or_create(
            book_id=id, profile_id=request.user.profile.id,
            defaults={'status': action}
        )
        return JsonResponse({'status': obj.status})

    return JsonResponse({"message": "not authorized"})


def rate_view(request):
    if request.user.is_authenticated() and request.method == "POST":
        book_id = request.POST.get('book_id')
        value = request.POST.get('value')
        user_id = request.user.id
        obj, created = Vote.objects.update_or_create(
            book_id=book_id, user_id=user_id,
            defaults={'value': value}
        )
        return JsonResponse({'created': created})
    return JsonResponse({"message": "not authorized"})


def follow_view(request):
    time.sleep(1)
    if request.user.is_authenticated() and request.method == "POST":
        model = request.POST.get('model')
        id = request.POST.get('id')
        status = request.POST.get('status')
        print(status)
        if model == 'category':
            obj, created = ProfileCategory.objects.update_or_create(
                category_id=id, profile_id=request.user.profile.id,
                defaults={'status': status}
            )
        elif model == 'author':
            obj, created = ProfileAuthor.objects.update_or_create(
                author_id=id, profile_id=request.user.profile.id,
                defaults={'status': status}
            )
        return JsonResponse({'status': obj.status})

    return JsonResponse({"message": "not authorized"})


def login_view(request):
    if request.method == "GET":
        return render(request, 'SimpleBookStore/login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid = True
        if not username or not password:
            valid = False
            messages.add_message(request, messages.INFO, "Username and password cannot be empty")
        user = User.objects.filter(username=username).first()
        if not user:
            valid = False
            messages.add_message(request, messages.INFO, "User does not exist")
        user = authenticate(username=username, password=password)
        if (user is not None) and valid:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('SimpleBookStore:index'))
            else:
                valid = False
                messages.add_message(request, messages.INFO, "User deactivated")
        else:
            valid = False
            messages.add_message(request, messages.INFO, "Incorrect password")
        if not valid:
            return HttpResponseRedirect(reverse("SimpleBookStore:login"))


def register(request):
    if request.method == "GET":
        return render(request, 'SimpleBookStore/register.html')
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        retype_password = request.POST.get("retype_password")
        valid = True
        if User.objects.filter(username=username).exists():
            valid = False
            messages.add_message(request, messages.INFO, "User already exists")
        if password != retype_password:
            valid = False
            messages.add_message(request, messages.INFO, "Password does not match")
        if not EMAIL_REGEX.match(email):
            valid = False
            messages.add_message(request, messages.INFO, "Invalid Email")
        if not valid:
            return HttpResponseRedirect(reverse("SimpleBookStore:register"))
        else:
            User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            user = authenticate(
                username=username,
                password=password
            )
            login(request, user)
            return HttpResponseRedirect(reverse("SimpleBookStore:index"))


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("SimpleBookStore:index"))
