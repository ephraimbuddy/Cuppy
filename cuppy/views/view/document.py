from pyramid.view import view_config


@view_config(route_name="view_doc", renderer="cuppy:templates/derived/document/document.mako")
def doc_view(request):
    context = request.context.obj
    return dict(document=context)

    

    

    