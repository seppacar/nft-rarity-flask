import requests

# TODO Fix all error handling, It is very messy right now, and maybe implement another API

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
def get_collection(collection_slug):
    url = f"https://api.opensea.io/api/v1/collection/{collection_slug}"
    try:
        response = requests.get(url, headers=headers)
        return response.json()  # Collection data
    except Exception:
        print("Connection Error")
        return


def get_asset(collection_slug, token_id):
    url = f'https://api.opensea.io/api/v1/assets?token_ids={token_id}&order_direction=desc&offset=0&limit=1&collection={collection_slug}'
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception:
        print("Connection Error")
        return


def get_trait_count(collection_data):
    trait_count = {}
    for trait_type in collection_data['collection']['traits']:
        trait_count[trait_type] = 0
        for trait in collection_data['collection']['traits'][trait_type]:
            trait_count[trait_type] += int(collection_data['collection']['traits'][trait_type][trait])
    return trait_count


# Get asset rarity for particular NFT dismiss missing traits
# TODO Improve rarity algorithm
def get_asset_rarity(token_id, collection_slug, trait_count):
    url = f'https://api.opensea.io/api/v1/assets?token_ids={token_id}&order_direction=desc&offset=0&limit=1&collection={collection_slug}'
    response = requests.get(url, headers=headers)
    rarity = 0
    try:
        for trait_type in response.json()['assets'][0]['traits']:
            rarity += 1 / (trait_type['trait_count'] / trait_count[trait_type['trait_type']])
    except Exception:
        print("Probably an API error")
    return rarity


# Get asset image URL
def get_asset_image(asset_json):
    try:
        image = asset_json['assets'][0]['image_original_url']
    except Exception:
        print("Can't get image")
        image = 'https://ipfs.io/ipfs/QmZ2ddtVUV1brVGjpq6vgrG6jEgEK3CqH19VURKzdwCSRf'
    if image.split(':')[0] == 'ipfs':
        image = 'http://ipfs.io/ipfs/' + image.split('//')[1]
    return image


def get_rarity(collection_slug, token_id):
    cdata = get_collection(collection_slug)
    traitc = get_trait_count(cdata)
    return get_asset_rarity(token_id, collection_slug, traitc)


def get_asset_data(collection_slug, token_id):
    data = {'image': get_asset_image(get_asset(collection_slug, token_id)),
            'rarity': get_rarity(collection_slug, token_id), '_id': token_id, '_slug': collection_slug}
    traits = get_asset(collection_slug, token_id)
    data['traits'] = {}
    try:
        for trait in traits['assets'][0]['traits']:
            data['traits'][trait['trait_type']] = {}
            data['traits'][trait['trait_type']] = trait['value']
    except Exception:
        print("This is getting messy I wil lfix")
    return data

