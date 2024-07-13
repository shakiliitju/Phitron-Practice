class SendMoneyView(TransactionCreateMixin):
    form_class = SendMoneyForm
    template_name = "transactions/sendmoney.html"
    title = "Send Money"
    success_url = reverse_lazy("transaction_report")

    def get_initial(self):
        initial = {"transaction_type": SEND_MONEY}
        return initial

    def form_valid(self, form):
        account_no = form.cleaned_data.get("account_no")
        amount = form.cleaned_data.get("amount")
        sender = self.request.user.account

        try:
            reciver = UserBankAccount.objects.get(account_no=account_no)
            reciver.balance += amount
            sender.balance -= amount
            reciver.save(update_fields=["balance"])
            sender.save(update_fields=["balance"])
            messages.success(self.request, "Send Money Successful")
            transaction_email(self.request.user, amount, self.title)
            transaction_email(reciver.user, amount, self.title)
            return super().form_valid(form)
        except UserBankAccount.DoesNotExist:
            form.add_error("account_no", "Invalid Account No")
            return super().form_invalid(form)
