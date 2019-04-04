from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
import os
from flask_login import current_user, login_required
# from models.user import User
# from models.image import Image
import braintree
from helpers import gateway

transactions_blueprint = Blueprint('transactions',
                            __name__,
                            template_folder='templates')


@transactions_blueprint.route('/donate', methods=['GET'])
def show():
    client_token = gateway.client_token.generate()
    return render_template('transactions/donate.html', client_token=client_token)

@transactions_blueprint.route('/donate/pay', methods=['POST'])
def pay():
    # take nonce and transaction value
    # send to braintree
    # on success, write value to db

    get_nonce = request.form.get('payment_method_nonce')
    get_amount = request.form.get('amount')

    result = gateway.transaction.sale({
    "amount": get_amount,
    "payment_method_nonce": get_nonce,
    "options": {
      "submit_for_settlement": True
    }})

    return redirect(url_for('transactions.show'))