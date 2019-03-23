from cuppy.views.view import doc_factory

def includeme(config):
    # Prefix all url with 'dashboard' at configuration
    #
    
    config.add_route('dashboard','index')
    config.add_route('page', 'page')
    config.add_route('add_doc', 'page/create*parent_id', pregenerator = pregen)
    config.add_route("edit_doc", 'page/*slug', factory=doc_factory)
    config.add_route("delete_doc", 'delete-page/*slug', factory=doc_factory)
    
    # Permission groups
    config.add_route('list_group', '/groups')
    config.add_route('add_group', '/groups/add')
    config.add_route('edit_group', '/groups/{id}/edit')
    config.add_route('delete_group','/groups/{id}/delete')

    # Users
    config.add_route('users', '/users')
    config.add_route('admin_edit_user', '/users/{id}/edit')
    config.add_route('add_to_group', '/users/{user_id}/{name}/add')
    config.add_route('remove_from_group', '/users/{user_id}/{name}/remove')

def pregen(request, elements, kw):
    kw.setdefault('parent_id', '')
    return elements, kw