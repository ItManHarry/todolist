#单条记录
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
#多条记录
def items_schema(items, pagination):
    return {
        'kind': 'Items Records',
        'items': [item_schema(item) for item in items],
        'first_page': 'N' if pagination.has_prev else 'Y',
        'last_page': 'N' if pagination.has_next else 'Y',
        'items_total': pagination.total
    }