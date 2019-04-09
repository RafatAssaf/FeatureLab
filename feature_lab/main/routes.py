from flask import Blueprint, render_template

main = Blueprint('main', __name__)

mock_requests = [
    {
        'title': 'Request# 1',
        'description': 'This feature should be accomplished',
        'client': {
            'name': 'CompanyX',
        },
        'priority': 2,
        'deadline': '2019-06-15',
        'product': {
            'name': 'Authentication'
        }
    },
    {
        'title': 'Request# 2',
        'description': 'This feature should be accomplished. This feature should be accomplished',
        'client': {
            'name': 'CompanyY',
        },
        'priority': 1,
        'deadline': '2019-10-15',
        'product': {
            'name': 'Search'
        }
    },
    {
        'title': 'Request# 3',
        'description': 'This feature',
        'client': {
            'name': 'CompanyZ',
        },
        'priority': 2,
        'deadline': '2019-06-15',
        'product': {
            'name': 'Main'
        }
    },
    {
        'title': 'Request# 4',
        'description': 'Adding Elastic search',
        'client': {
            'name': 'CompanyA',
        },
        'priority': 5,
        'deadline': '2019-04-15',
        'product': {
            'name': 'Search'
        }
    },
    {
        'title': 'Request# 1',
        'description': 'This feature should be accomplished',
        'client': {
            'name': 'CompanyX',
        },
        'priority': 1,
        'deadline': '2019-06-15',
        'product': {
            'name': 'Authentication'
        }
    },
    {
        'title': 'Request# 2',
        'description': 'This feature should be accomplished. This feature should be accomplished',
        'client': {
            'name': 'CompanyY',
        },
        'priority': 3,
        'deadline': '2019-10-15',
        'product': {
            'name': 'Search'
        }
    },
    {
        'title': 'Request# 3',
        'description': 'This feature',
        'client': {
            'name': 'CompanyZ',
        },
        'priority': 4,
        'deadline': '2019-06-15',
        'product': {
            'name': 'Main'
        }
    },
    {
        'title': 'Request# 4',
        'description': 'Adding Elastic search',
        'client': {
            'name': 'CompanyA',
        },
        'priority': 3,
        'deadline': '2019-04-15',
        'product': {
            'name': 'Search'
        }
    },
]


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', requests=mock_requests, title='Home')


@main.route('/about')
def about():
    return render_template('about.html', title='About')
