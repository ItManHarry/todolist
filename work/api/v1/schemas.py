def item_schema(item):
    return {
        'id': item.id,
        #'self': url_for('.item', item_id=item.id, _external=True),
        'kind': 'Item',
        'title': item.title,
        'body': item.body,
        'done': item.done,
        'author': {
            'id': item.author.id,
            #'url': url_for('.user', _external=True),
            'name': item.author.name,
            'kind': 'User'
        }
    }