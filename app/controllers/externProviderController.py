import requests
from app.model.externProvider import ExternProvider
from app.model.point import ExternPoint
from app.model.category import ExternCategory

def get_extern_points():

    extern_points = []

    try:
        r1 = requests.get(
            url = provider_1.endpoints['points']['url'],
            params = provider_1.endpoints['points']['params']
        )
        r1.raise_for_status()
        provider_1_points = r1.json()
        adapted_p1_points = adapt_p1_points(provider_1_points)
        extern_points = extern_points + adapted_p1_points
    except requests.exceptions.HTTPError as err:
        print(err, flush=True)

    try:
        r2 = requests.get(
            url = provider_2.endpoints['points']['url'],
            params = provider_2.endpoints['points']['params']
        )
        r2.raise_for_status()
        provider_2_points = r2.json()
        adapted_p2_points = adapt_p2_points(provider_2_points)
        extern_points = extern_points + adapted_p2_points
    except requests.exceptions.HTTPError as err:
        print(err, flush=True)

    return extern_points

def get_extern_categories():

    extern_categories = []

    try:
        r1 = requests.get(
            url = provider_1.endpoints['categories']['url'],
            params = provider_1.endpoints['categories']['params']
        )
        r1.raise_for_status()
        provider_1_categories = r1.json()
        adapted_p1_categories = adapt_p1_categories(provider_1_categories)
        extern_categories = extern_categories + adapted_p1_categories
    except requests.exceptions.HTTPError as err:
        print(err, flush=True)

    try:
        r2 = requests.get(
            url = provider_2.endpoints['categories']['url'],
            params = provider_2.endpoints['categories']['params']
        )
        r2.raise_for_status()
        provider_2_categories = r2.json()
        adapted_p2_categories = adapt_p2_categories(provider_2_categories)
        extern_categories= extern_categories + adapted_p2_categories
    except requests.exceptions.HTTPError as err:
        print(err, flush=True)

    return extern_categories


#### PROVIDERS DEFINITIONS #####

## Provider 1 ##

provider_1_api_url = 'https://pointerest-arq.herokuapp.com'
provider_1 = ExternProvider(
    name = 'pointerest-arq',
    site_url = provider_1_api_url,
    api_url = provider_1_api_url,
    endpoints = {
        'points' : dict( url = provider_1_api_url + '/points.json',
                         params = {}),
        'categories' : dict( url = provider_1_api_url + '/categories.json',
                             params = {})
    }
)

def adapt_p1_points(points):
    return list(map(
        lambda p: ExternPoint(
            position = {'lat':p['lat'],'lng':p['long']},
            name = p['name'],
            description = p['description'],
            image = p['img'],
            categoryId = p['category']['id'],
            categoryName = p['category']['name'],
            provider = dict( name=provider_1.name,
                             site_url=provider_1.site_url,
                             poi_abs_id= provider_1.name + "_point_" + str(p['id']),
                             cat_abs_id= provider_1.name + "_category_" + str(p['category']['id'])
                           )
        ).__dict__,
        points))

def adapt_p1_categories(categories):
    ext_categories = []
    for c in categories:
        if c['status'] == "APPROVED":
            ext_categories.append( ExternCategory(
                title = c['name'],
                icon = c['icon'],
                provider = dict( name=provider_1.name,
                                 site_url=provider_1.site_url,
                                 cat_abs_id=provider_1.name + "_category_" + str(c['id'])
                               )
            ).__dict__)
    return ext_categories

################

## Provider 2 ##
provider_2_url = 'http://arq-web.herokuapp.com'
provider_2_api_url = 'http://arq-web.herokuapp.com' + '/api'
provider_2 = ExternProvider(
    name = 'arq-web',
    site_url = provider_2_url,
    api_url = provider_2_api_url,
    endpoints = {
        'points' : dict( url = provider_2_api_url + '/points',
                         params = dict(categories='', title='')),
        'categories' : dict( url = provider_2_api_url + '/categories',
                             params = dict(hidden=False, state='APPROVED'))
    }
)

def adapt_p2_points(points):
    return list(map(
        lambda p: ExternPoint(
            position = {'lat':p['latitude'],'lng':p['longitude']},
            name = p['title'],
            description = p['description'],
            image =  provider_2.site_url + p['imageUrl'],
            categoryId = p['category']['id'],
            categoryName = p['category']['name'],
            provider = dict ( name=provider_2.name,
                              site_url=provider_2.site_url,
                              poi_abs_id= provider_2.name + "_point_" + str(p['id']),
                              cat_abs_id= provider_2.name + "_category_" + str(p['category']['id'])
                            )
        ).__dict__,
        points))

def adapt_p2_categories(categories):
    return list(map(
        lambda c: ExternCategory(
            title = c['name'],
            icon =  provider_2.site_url + c['logoUrl'],
            provider = dict ( name=provider_2.name,
                              site_url=provider_2.site_url,
                              cat_abs_id=provider_2.name + "_category_" + str(c['id'])
                            )
        ).__dict__,
        categories))

####################
