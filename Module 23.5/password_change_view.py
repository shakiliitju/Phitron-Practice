class UserPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "accounts/password_change.html"

    def get_success_url(self):
        message = render_to_string(
            "accounts/mail.html",
            {
                "user": self.request.user,
            },
        )
        to_email = [self.request.user.email]
        if isinstance(message, tuple):
            message = "".join(message)
        send_email = EmailMultiAlternatives(
            subject="Password Change",
            body="",
            to=to_email,
        )
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        return reverse_lazy("profile")

    def form_valid(self, form):
        messages.success(self.request, "Password Change Successful")
        return super().form_valid(form)
