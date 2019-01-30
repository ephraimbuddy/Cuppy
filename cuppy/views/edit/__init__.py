from cuppy.views.document import doc_factory

def includeme(config):
    # Prefix all url with 'dashboard' at configuration
    #
    
    config.add_route('dashboard','index')
    config.add_route('add_doc', 'page/create')
    config.add_route("edit_doc", 'page/{slug}/update', factory = doc_factory, traverse="{slug}")
    config.add_route("delete_doc", 'page/{slug}/delete', factory = doc_factory, traverse="{slug}")