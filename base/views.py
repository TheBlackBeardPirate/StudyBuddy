from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Topic, Room, Messages, get_user_model
from .forms import MyUserCreationForm, UserForm, RoomForm


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('login').lower()
        password = request.POST.get('password')

        try:
            user_model = get_user_model()
            user = user_model.objects.get(email=email)
        except Exception as err:
            redirect('login')
            messages.error(request, 'Wrong username or password!')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong username or password!')

    context = {'page': 'login'}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''

    rooms = Room.objects.filter(
        Q(topics__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    topics_count = topics.count()
    rooms_count = rooms.count()
    msgs = Messages.objects.filter(Q(room__topics__name__icontains=q))[0:5]

    context = {'rooms': rooms, 'rooms_count': rooms_count, 'topics_count': topics_count, 'topics': topics, 'msgs': msgs}
    return render(request, 'base/index.html', context)


@login_required(login_url='login')
def creat_room(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topics=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )

        return redirect('home')

    context = {'topics': topics, 'form': form}
    return render(request, 'base/create-room.html', context)


def room_page(request, pk):
    room = Room.objects.get(id=pk)
    msgs = room.messages_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        Messages.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'msgs': msgs, 'participants': participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    msg = Messages.objects.get(id=pk)
    room = msg.room

    if request.user != msg.user:
        return HttpResponse('You are not allowed to do it!')

    if request.method == 'POST':
        msg.delete()
        return redirect('room', pk=room.id)

    context = {'msg': msg}
    return render(request, 'base/delete.html', context)


def profile_page(request, pk):
    user_model = get_user_model()
    user = user_model.objects.get(id=pk)
    msgs = user.messages_set.all()
    rooms = Room.objects.filter(host=user)
    topics = Topic.objects.all()
    topics_count = topics.count()
    context = {'topics': topics, 'topics_count': topics_count, 'msgs': msgs, 'user': user, 'rooms': rooms}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def edit_user(request):
    user = request.user
    form = UserForm(instance=user)
    context = {'form': form}

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()

            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 and password2:
                user.set_password(password1)
                user.save()
                login(request, user)
            elif password1 == '' and password2 == '':
                user.set_password(password1)
                user.save()
                login(request, user)
            else:
                messages.error(request, 'An error occured during the process!')
                return redirect('user-profile', pk=user.id)

            return redirect('user-profile', pk=user.id)
        else:
            messages.error(request, 'An error occured during the process!')

    return render(request, 'base/edit-user.html', context)


def topics_page(request):
    topics = Topic.objects.all()

    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activity_page(request):
    msg = Messages.objects.all()

    context = {'msg': msg}
    return render(request, 'base/activity.html', context)


def register_page(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during the registration!')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)
