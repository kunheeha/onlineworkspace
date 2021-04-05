import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.models import User
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
        'products': products
    }

    return render(request, 'users/profile.html', context)


class SuccessView(TemplateView):
    template_name = 'users/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workspaces'] = self.request.user.profile.workspaces_number
        context['files'] = self.request.user.profile.files_number
        return context


class CancelView(TemplateView):
    template_name = 'users/cancel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workspaces'] = self.request.user.profile.workspaces_number
        context['files'] = self.request.user.profile.files_number
        return context


class CreateCheckoutSessionView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CreateCheckoutSessionView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        quantity = self.kwargs['quantity']
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
                    'quantity': quantity,
                },
            ],
            metadata={
                'user_id': self.request.user.id,
                'product_id': product.id,
                'quantity': quantity
            },
            mode='payment',
            success_url=DOMAIN + 'success/',
            cancel_url=DOMAIN + 'cancel/',
        )
        return JsonResponse({'id': checkout_session.id})


def fulfill_order(session):
    purchaser_email = session['customer_details']['email']
    user_id = session['metadata']['user_id']
    product_id = session['metadata']['product_id']
    quantity = session['metadata']['quantity']

    product = Product.objects.get(id=product_id)

    fulfill_user = User.objects.get(id=user_id)
    if product.name == 'Workspace':
        fulfill_user.profile.workspaces_number += int(quantity)
        fulfill_user.profile.save()
    elif product.name == 'File Upload':
        fulfill_user.profile.files_number += int(quantity)
        fulfill_user.profile.save()

    send_mail(
        subject='Purchase from OnlineWorkspace',
        message=f'Thank you for your purchase, you bought {quantity} of {product.name}(s)',
        recipient_list=[purchaser_email],
        from_email=settings.EMAIL_HOST_USER
    )
    print('did it work?')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)
