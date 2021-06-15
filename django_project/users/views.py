from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm, ProfilePictureForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Registration success for {username}')
            return redirect('blog-homepage')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_picture_form = ProfilePictureForm(request.POST,
                                                  request.FILES,
                                                  instance=request.user.profile)
        if user_form.is_valid() and profile_picture_form.is_valid():
            user_form.save()
            profile_picture_form.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Profile updated for the user {username}')
            return redirect('users-profile')

    else:
        user_form = UserProfileForm(instance=request.user)
        profile_picture_form = ProfilePictureForm()
    return render(request, 'users/profile.html',
                  {'user_form': user_form,
                   'profile_picture_form': profile_picture_form})

class UserPasswordChangeView(PasswordChangeView):
    model = User
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users-profile')



