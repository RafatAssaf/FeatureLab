from flask import Blueprint, render_template, flash, redirect, url_for, jsonify, request, abort
from flask_login import login_required, current_user
from feature_lab import db
from feature_lab.clients.forms import CreateRequestForm, CreateProductForm, CreateClientForm
from feature_lab.models import Client, Product, ProductArea, FeatureRequest, FeatureRequestState
from sqlalchemy import desc

clients = Blueprint('clients', __name__)


""" Client endpoints """


@clients.route('/client/<int:client_id>')
@login_required
def client(client_id):  # client page
    client = Client.query.get_or_404(int(client_id))
    return render_template('client.html', client=client)


@clients.route('/clients')
@login_required
def clients_list(): # clients list page
    all_clients = Client.query.filter_by(user_id=current_user.id).all()
    return render_template('clients.html', clients=all_clients)


@clients.route('/create_client', methods=['GET', 'POST'])
@login_required
def create_client():
    form = CreateClientForm()
    if form.validate_on_submit():
        new_client = Client(form.name.data,
                            form.email.data,
                            form.bio.data,
                            form.phone_number.data,
                            current_user.id)
        db.session.add(new_client)
        db.session.commit()
        flash('Client {} was created successfully!'.format(form.name.data), 'success')
        return redirect(url_for('main.home'))
    else:
        return render_template('create_client.html', form=form)


@clients.route('/client/<int:client_id>/update', methods=['GET', 'POST'])
@login_required
def update_client(client_id):
    form = CreateClientForm()
    client = Client.query.get_or_404(client_id)
    if request.method == 'GET':
        # populate the form with client data
        form.name.data = client.name
        form.email.data = client.email
        form.bio.data = client.bio
        form.phone_number.data = client.phone_number
        return render_template('create_client.html', form=form)
    elif form.validate_on_submit():
        # update clients data
        client.name = form.name.data
        client.email = form.email.data
        client.bio = form.bio.data
        client.phone_number = form.phone_number.data
        db.session.commit()
        return redirect(url_for('clients.client', client_id=client.id))


@clients.route('/client/<int:client_id>/delete', methods=['POST'])
@login_required
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    if client.user != current_user:
        abort(403)
    # get client products
    client_products = Product.query.filter_by(owner_id=client_id).all()
    client_requests = []
    # get each product requests
    for product in client_products:
        client_requests += FeatureRequest.query.filter_by(product_id=product.id).all()
    client_products_areas = []
    # get each product areas
    for product in client_products:
        client_products_areas += ProductArea.query.filter_by(product_id=product.id).all()

    # delete client products areas
    for area in client_products_areas:
        db.session.delete(area)
    # delete client requests
    for request in client_requests:
        db.session.delete(request)
    # delete client products
    for product in client_products:
        db.session.delete(product)
    # and finally delete the client
    db.session.delete(client)

    db.session.commit()
    flash('Client has been deleted successfully', 'success')
    return redirect(url_for('clients.clients_list'))


""" Products endpoints """


@clients.route('/product/<int:product_id>')
@login_required
def product(product_id):
    product_data = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product_data)


@clients.route('/create_product/<int:client_id>', methods=['GET', 'POST'])
@login_required
def create_product(client_id):
    form = CreateProductForm()
    if form.validate_on_submit():
        new_product = Product(form.name.data,
                              form.description.data,
                              client_id)
        db.session.add(new_product)
        db.session.commit()
        # split the areas string by commas
        areas = form.areas.data.split(',')
        # and create a product area for each comma separated value
        for area in areas:
            new_area = ProductArea(area, new_product.id)
            db.session.add(new_area)

        db.session.commit()
        flash('Product {} has been successfully created!'.format(form.name.data), 'success')
        return redirect(url_for('clients.client', client_id=client_id))
    else:
        return render_template('create_product.html', form=form)


@clients.route('/product/<product_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    form = CreateProductForm()
    product = Product.query.get_or_404(product_id)
    if request.method == 'GET':
        form.name.data = product.name
        form.description.data = product.description
        form.areas.data = ','.join([a.name for a in product.areas])
        return render_template('create_product.html', form=form)
    elif form.validate_on_submit():
        # update product with new data
        product.name = form.name.data
        product.description = form.description.data
        old_areas = ProductArea.query.filter_by(product_id=product_id).all()
        # delete old areas
        for area in old_areas:
            db.session.delete(area)
        # create new areas
        new_areas = form.areas.data.split(',')
        for area in new_areas:
            new_area = ProductArea(area, product.id)
            db.session.add(new_area)
        # commit changes
        db.session.commit()
        return redirect(url_for('clients.product', product_id=product.id))


@clients.route('/product/<int:product_id>/update', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    # abort if the user is not authorized to delete the product
    if product.owner.user != current_user:
        abort(403)
    # delete the product areas first
    areas = ProductArea.query.filter_by(product_id=product_id)
    requests = FeatureRequest.query.filter_by(product_id=product_id)
    # delete the product's areas
    for area in areas:
        db.session.delete(area)
    # delete the products requests
    for request in requests:
        db.session.delete(request)
    # then delete the product itself
    db.session.delete(product)

    db.session.commit()
    flash('Product has been successfully deleted', 'success')
    return redirect(url_for('clients.client', client_id=product.owner_id))


@clients.route('/products/<client_id>')
@login_required
def products(client_id): # data endpoint to get a JSON response with client's products
    clients_products = Product.query.filter_by(owner_id=client_id).all()
    products_data = []
    for product in clients_products:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'owner_id': client_id
        })
    if products_data:
        return jsonify({'products': products_data})
    else:
        return jsonify({'error': 'Client not found!'})


@clients.route('/product_areas/<product_id>')
@login_required # data endpoint to get a product's areas
def product_areas(product_id):
    areas = ProductArea.query.filter_by(product_id=product_id).all()
    areas_data = []
    for area in areas:
        areas_data.append({
            'id': area.id,
            'name': area.name,
            'product_id': product_id
        })
    if areas:
        return jsonify({'areas': areas_data})
    else:
        return jsonify({'error': 'Product Not Found'})


""" Feature requests endpoints """


@clients.route('/request/<int:request_id>')
@login_required
def feature_request(request_id):  # request page
    request = FeatureRequest.query.get_or_404(request_id)
    # extract the enum values of request states
    request_states = list(map(lambda s: s, FeatureRequestState))
    return render_template('request.html', request=request, request_states=request_states)


@clients.route('/create_request', methods=['GET', 'POST'])
@login_required
def create_request():
    form = CreateRequestForm()
    if request.method == 'GET':
        # query select fields data
        clients = Client.query.filter_by(user_id=current_user.id).filter(Client.products.any()).all()
        if not clients:  # check if we have client's to add requests to at first place
            flash('You do not have any clients with products yet', 'info')
            return redirect(url_for('clients.clients_list'))
        products = Product.query.filter_by(owner_id=clients[0].id).all()
        areas = ProductArea.query.filter_by(product_id=products[0].id).all()
        # create the choices for select fields
        form.client.choices = [(client.id, client.name) for client in clients]
        form.product.choices = [(product.id, product.name) for product in products]
        form.product_area.choices = [(area.name, area.name) for area in areas]
        return render_template('create_request.html', form=form)
    elif form.validate_on_submit():
        # get all product's requests ordered by priority
        prioirity_ordered_requests = FeatureRequest.query\
            .filter_by(product_id=form.product.data).order_by(FeatureRequest.priority).all()
        if not prioirity_ordered_requests:
            form.priority.data = 1  # ensure the first client has priority 1
        elif form.priority.data > prioirity_ordered_requests[-1].priority:
            form.priority.data = prioirity_ordered_requests[-1].priority + 1  # to avoid missing priorities
        else:  # else we have to reorder
            for req in prioirity_ordered_requests[form.priority.data - 1:]:
                req.priority += 1
        new_feature_request = FeatureRequest(form.title.data,
                                             form.description.data,
                                             form.created_at.data,
                                             form.target_date.data,
                                             form.product_area.data,
                                             form.product.data,
                                             form.client.data,
                                             form.priority.data)
        db.session.add(new_feature_request)
        db.session.commit()
        flash('Request was created successfully!', 'success')
        return redirect(url_for('main.home'))
    else:
        flash('Something went wrong', 'danger')
        return redirect(url_for('clients.create_request'))


@clients.route('/request/<int:request_id>/update', methods=['GET', 'POST'])
@login_required
def update_request(request_id):
    request_data = FeatureRequest.query.get_or_404(request_id)
    # creating the form and passing the default values for client,product,product_area
    form = CreateRequestForm(client=request_data.client_id,
                             product=request_data.product_id,
                             product_area=request_data.product_area)
    if request.method == 'GET':
        # fetching the choices data for select fields
        clients = Client.query.filter_by(user_id=current_user.id).filter(Client.products.any()).all()
        products = Product.query.filter_by(owner_id=request_data.client_id).all()
        areas = ProductArea.query.filter_by(product_id=request_data.product_id).all()

        # create and assign the choices for their corresponding fields
        form.client.choices = [(client.id, client.name) for client in clients]
        form.product.choices = [(product.id, product.name) for product in products]
        form.product_area.choices = [(area.name, area.name) for area in areas]

        # populate the rest of the form with request data
        form.title.data = request_data.title
        form.description.data = request_data.description
        form.created_at.data = request_data.created_at
        form.target_date.data = request_data.target_date
        form.priority.data = request_data.priority
        return render_template('create_request.html', form=form)
    elif form.validate_on_submit():
        # update request data with form data and commit the changes to the database
        request_data.title = form.title.data
        request_data.description = form.description.data
        request_data.created_at = form.created_at.data
        request_data.target_date = form.target_date.data
        request_data.client_id = form.client.data
        request_data.product_id = form.product.data
        request_data.product_area = form.product_area.data
        request_data.priority = form.priority.data
        db.session.commit()
        flash('Feature request has been updated successfully', 'success')
        return redirect(url_for('clients.feature_request', request_id=request_id))
    else:
        flash('Something went wrong', 'danger')
        return redirect(url_for('clients.update_request', request_id=request_id))


@clients.route('/request/<int:request_id>/delete', methods=['POST'])
@login_required
def delete_request(request_id):
    request_data = FeatureRequest.query.get_or_404(request_id)
    # abort if the user is not authorized to delete the product
    if request_data.product.owner.user != current_user:
        abort(403)
    db.session.delete(request_data)
    db.session.commit()
    flash('Product has been successfully deleted', 'success')
    return redirect(url_for('clients.client', client_id=request_data.client_id))


@clients.route('/request/<int:request_id>/update_state', methods=['POST'])
@login_required
def update_request_state(request_id):
    request_data = FeatureRequest.query.get_or_404(request_id)
    next_state = request.get_json().get('state')
    request_data.state = FeatureRequestState[next_state]
    db.session.commit()
    flash('Request state successfully updated to {}'.format(FeatureRequestState[next_state].value), 'success')
    return redirect(url_for('clients.feature_request', request_id=request_id))
