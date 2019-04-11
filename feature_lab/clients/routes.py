from flask import Blueprint, render_template, flash, redirect, url_for, jsonify, request
from feature_lab.clients.forms import CreateRequestForm, CreateClientForm

clients = Blueprint('clients', __name__)

clients_data = [
    {
        'name': 'CompanyX',
        'products': [
            {
                'name': 'Prod-A',
                'areas': ['Search', 'User Account']
            },
            {
                'name': 'Prod-B',
                'areas': ['Map']
            }
        ],
        'email': 'companyx@example.com',
        'phone_number': '+1 293 987 872',
        'created_at': '2017-09-10'
    },
    {
        'name': 'CompanyY',
        'products': [
            {
                'name': 'Prod-C',
                'areas': ['Landing', 'Notification']
            },
            {
                'name': 'Prod-D',
                'areas': ['Onboarding']
            }
        ],
        'email': 'companyy@example.com',
        'phone_number': '+1 123 987 456',
        'created_at': '2015-05-10'
    }
]


@clients.route('/request')
def feature_request():
    return render_template('request.html')


@clients.route('/clients')
def clients_list():
    return render_template('clients.html', clients=clients_data)


@clients.route('/products/<client>')
def products_list(client):
    return "products list: " + client


@clients.route('/create_client', methods=['GET', 'POST'])
def create_client():
    form = CreateClientForm()
    if form.validate_on_submit():
        flash('Client {} was created successfully!'.format(form.name.data), 'success')
        return redirect(url_for('main.home'))
    else:
        return render_template('create_client.html', form=form)


@clients.route('/create_request', methods=['GET', 'POST'])
def create_request():
    form = CreateRequestForm()
    form.client.choices = [(client['name'], client['name']) for client in clients_data]
    form.product.choices = [(product['name'], product['name']) for product in clients_data[0].get('products')]
    form.product_area.choices = [(area, area) for area in clients_data[0]['products'][0]['areas']]

    if form.validate_on_submit():
        flash('Request was created successfully!', 'success')
        return redirect(url_for('main.home'))
    else:
        return render_template('create_request.html', form=form)


@clients.route('/products/<client>')
def products(client):
    selected_client = None
    for current_client in clients_data:
        if current_client['name'] == client:
            selected_client = current_client
            break

    if selected_client:
        return jsonify({'products': selected_client['products']})
    else:
        return jsonify({'error': 'Client no found!'})


@clients.route('/product_areas/<product>')
def product_areas(product):
    selected_product = None
    for current_client in clients_data:
        for current_product in current_client['products']:
            if current_product['name'] == product:
                selected_product = current_product
                break

    if selected_product:
        return jsonify({'areas': selected_product['areas']})
    else:
        return {'error': 'Product Not Found'}
