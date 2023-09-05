
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
@login_required
def send_verification_email(request):
    current_site = get_current_site(request)
    mail_subject = "Подтвердите свою почту"
    message = render_to_string('users/verification_email.html', {
        'user': request.user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
        'token': default_token_generator.make_token(request.user)
    })
    send_mail(mail_subject, message, 'sendinfoforauth@gmail.com', [request.user.email])

    return render(request, 'users/verification_sent.html')

@login_required
def verify_email(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = get_user_model().objects.get(pk=uid)
    except:
        user = None

    else:
        if user is not None and default_token_generator.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return render(request, 'users/success_verification.html')
        else:
            return render(request, 'users/error_verification.html')

def suc_pass(request):
    return render(request, 'users/password_change_done.html')

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    def get_object(self, queryset=None):
        return self.request.user

@login_required
def change_password(request):
    if request.method == 'POST':
        user = request.user
        generated_password = make_password('12')
        user.set_password(generated_password)
        user.save()
        return render(request, 'users/password_change_done.html')
    else:
        return render(request, 'users/generate_password.html')
