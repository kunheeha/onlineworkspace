import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, UserUpdateForm
from .models import Profile, Product
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username}, Please log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    left_workspaces = request.user.profile.workspaces_number
    left_files = request.user.profile.files_number
    products = Product.objects.all()

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been updated')
            return redirect('profile')

    form = UserUpdateForm(instance=request.user)

    context = {
        'workspaces': left_workspaces,
        'files': left_files,
        'form': form,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        'products': products
    }

    return render(request, 'users/profile.html', context)


class SuccessView(TemplateView):
    template_name = 'users/success.html'


class CancelView(TemplateView):
    template_name = 'users/cancel.html'


class CreateCheckoutSessionView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CreateCheckoutSessionView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        product = Product.objects.get(id=product_id)
        DOMAIN = 'http://127.0.0.1:8000/'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'gbp',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=DOMAIN + '/success/',
            cancel_url=DOMAIN + '/cancel/',
        )
        return JsonResponse({'id': checkout_session.id})
