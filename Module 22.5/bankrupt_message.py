class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = "Withdraw Money"

    def get_initial(self):
        initial = {"transaction_type": WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get("amount")
        bank_balance = UserBankAccount.objects.aggregate(total_balance=Sum("balance"))[
            "total_balance"
        ]
        if bank_balance < amount:
            messages.warning(self.request, "bank is bankrupt")
        else:
            self.request.user.account.balance -= form.cleaned_data.get("amount")
            self.request.user.account.save(update_fields=["balance"])

            messages.success(
                self.request,
                f'Successfully withdrawn {"{:,.2f}".format(float(amount))}$ from your account',
            )
            transaction_email(self.request.user, amount, self.title)
        return super().form_valid(form)
