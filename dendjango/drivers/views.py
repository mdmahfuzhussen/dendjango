from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import BookingForm, ReviewForm, SignupForm
from .models import Review


def home(request):
    booking_form = BookingForm(initial={
        'name': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
    } if request.user.is_authenticated else None)

    reviews = Review.objects.filter(is_published=True)

    return render(request, 'drivers/home.html', {
        'booking_form': booking_form,
        'review_form': ReviewForm(),
        'reviews': reviews,
    })


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('drivers:home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Signup successful. You are now logged in.')
            return redirect('drivers:home')
    else:
        form = SignupForm()

    return render(request, 'drivers/signup.html', {
        'form': form,
    })


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('drivers:home')


@login_required
def booking(request):
    if request.method != 'POST':
        return redirect('drivers:home')

    form = BookingForm(request.POST)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.save()
        messages.success(request, 'Your lesson booking has been received. Thank you!')
        return redirect('drivers:home')

    return render(request, 'drivers/home.html', {
        'booking_form': form,
        'review_form': ReviewForm(),
        'reviews': Review.objects.filter(is_published=True),
    })


@login_required
def submit_review(request):
    if request.method != 'POST':
        return redirect('drivers:home')

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.save()
        messages.success(request, 'Your review has been published successfully.')
    else:
        messages.error(request, 'Please enter a valid review.')

    return redirect('drivers:home')
