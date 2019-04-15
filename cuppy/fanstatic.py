from fanstatic import Library, Resource, Group, Inclusion
from js.jquery_form import jquery_form
from cuppystatic import adminlte_skin_blue_css
from cuppystatic import adminlte_js


cuppylib = Library('cuppy','static')


views_css = Resource(cuppylib, 
                        "views.css",
                         minified='views.min.css',
                        depends=[adminlte_skin_blue_css],
                        dont_bundle=True,
                        bottom = False)

edit_css = Resource(cuppylib,
                     "edit.css",
                     minified='edit.min.css',
                      depends=[adminlte_skin_blue_css],
                      dont_bundle=True,
                      bottom = False)


views_js = Resource(cuppylib,
                     "views.js", 
                     minified='views.min.js',
                     depends=[adminlte_js],
                     bottom=True)

edit_js = Resource(cuppylib,
                 'edit.js', 
                 minified='edit.min.js',
                 depends=[adminlte_js,jquery_form],
                 bottom=True)

view_needed=Group([views_css, views_js])
edit_needed = Group([edit_css, edit_js])