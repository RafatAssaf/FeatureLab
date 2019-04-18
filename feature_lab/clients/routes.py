from flask import Blueprint, render_template, flash, redirect, url_for, jsonify, request
from flask_login import login_required
from feature_lab import db
from feature_lab.clients.forms import CreateRequestForm, CreateProductForm, CreateClientForm
from feature_lab.models import Client, Product, FeatureRequest

clients = Blueprint('clients', __name__)

clients_data = [
    {
        'name': 'CompanyX',
        'products': [
            {
                'name': 'Prod-A',
                'description': 'some testing description to display on the page',
                'areas': ['Search', 'User Account']
            },
            {
                'name': 'Prod-B',
                'description': 'some testing description to display on the page',
                'areas': ['Map']
            }
        ],
        'email': 'companyx@example.com',
        'phone_number': '+1 293 987 872',
        'created_at': '2017-09-10',
        'priority': 1
    },
    {
        'name': 'CompanyY',
        'products': [
            {
                'name': 'Prod-C',
                'description': 'some testing description to display on the page',
                'areas': ['Landing', 'Notification']
            },
            {
                'name': 'Prod-D',
                'description': 'some testing description to display on the page',
                'areas': ['Onboarding']
            }
        ],
        'email': 'companyy@example.com',
        'phone_number': '+1 123 987 456',
        'created_at': '2015-05-10',
        'priority': 2
    }
]

request_data = {
    'title': 'Adding auto complete',
    'description': 'Adding auto complete functionality to search pages',
    'client': 'CompanyX',
    'product': 'Prod-A',
    'product_area': 'Search',
    'target_date': '2019-15-8',
    'created_at': '2019-12-4'
}


""" Client endpoints """


@clients.route('/client/<client_id>')
@login_required
def client(client_id):
    client = Client.query.get_or_404(int(client_id))
    return render_template('client.html', client=client)


@clients.route('/clients')
@login_required
def clients_list():
    all_clients = Client.query.all()
    return render_template('clients.html', clients=all_clients)


@clients.route('/create_client', methods=['GET', 'POST'])
@login_required
def create_client():
    form = CreateClientForm()
    if form.validate_on_submit():
        client = Client(form.name.data,
                        form.email.data,
                        form.bio.data,
                        form.priority.data,
                        form.phone_number.data)
        db.session.add(client)
        db.session.commit()
        flash('Client {} was created successfully!'.format(form.name.data), 'success')
        return redirect(url_for('main.home'))
    else:
        return render_template('create_client.html', form=form)


""" Products endpoints """


@clients.route('/product/<product_id>')
@login_required
def product(product_id):
    product_data = clients_data[0]['products'][0]
    product_data['requests'] = [request_data]
    return render_template('product.html', product=product_data)


@clients.route('/create_product', methods=['GET', 'POST'])
@login_required
def create_product():
    form = CreateProductForm()
    form.client.choices = [(client['name'], client['name']) for client in clients_data]  # initialize with clients
    if form.validate_on_submit():
        flash('Product {} for client {} has been successfully created!'.format(form.name.data, form.client.data))
        return redirect(url_for('clients.client', client_id=form.client.data))
    else:
        return render_template('create_product.html', form=form)


@clients.route('/products/<client>')
@login_required
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
@login_required
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


""" Feature requests endpoints """


@clients.route('/request/<request_id>')
@login_required
def feature_request(request_id):
    return render_template('request.html', request=request_data)


@clients.route('/create_request', methods=['GET', 'POST'])
@login_required
def create_request():
    form = CreateRequestForm()
    form.client.choices = [(client['name'], client['name']) for client in clients_data]
    form.product.choices = [(product['name'], product['name']) for product in clients_data[0].get('products')]
    form.product_area.choices = [(area, area) for area in clients_data[0]['products'][0]['areas']]

    if form.validate_on_submit():
        flash('Request was created successfully!', 'success')
        print(form.target_date.data)
        return redirect(url_for('main.home'))
    else:
        return render_template('create_request.html', form=form)
