from cuppy.views.document import doc_factory

def includeme(config):
    # Prefix all url with 'dashboard' at configuration
    #
    
    config.add_route('dashboard','index')
    config.add_route('page', 'page')
    config.add_route('add_doc', 'page/create*parent_id', pregenerator = pregen)
    config.add_route("edit_doc", 'page/*slug', factory=doc_factory)
    config.add_route("delete_doc", 'page/{id}/delete')


def pregen(request, elements, kw):
    kw.setdefault('parent_id', '')
    return elements, kw