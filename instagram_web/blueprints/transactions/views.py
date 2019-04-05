from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
import os
from flask_login import current_user, login_required
import braintree
from helpers import gateway, find_transaction, transact
import helpers

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


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

    # transaction = helpers.find_transaction('6e90bazd')
    if result.is_success or result.transaction:
        return redirect(url_for('transactions.success', transaction_id=result.transaction.id))
    else:
        return redirect(url_for('transactions.show'))



@transactions_blueprint.route('/donate/<transaction_id>', methods=['GET'])
def success(transaction_id):
    # r = result
    # # breakpoint()
    # transaction = helpers.find_transaction(transaction.id)

    message = Mail(
        from_email='from_email@example.com',
        to_emails='chibijade99@gmail.com',
        subject='Sending with SendGrid is Fun',
        html_content=f"""
            <strong>and easy to do anywhere, even with Python</strong>
            <p>afklhaslgjljlasjla {transaction_id}</p>
            """
        )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

    return render_template('transactions/receipt.html', transaction_id=transaction_id)













# @app.route('/checkouts/<transaction_id>', methods=['GET'])
# def show_checkout(transaction_id):
#     transaction = find_transaction(transaction_id)
#     result = {}
#     if transaction.status in TRANSACTION_SUCCESS_STATUSES:
#         result = {
#             'header': 'Sweet Success!',
#             'icon': 'success',
#             'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
#         }
#     else:
#         result = {
#             'header': 'Transaction Failed',
#             'icon': 'fail',
#             'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
#         }

#     return render_template('checkouts/show.html', transaction=transaction, result=result)