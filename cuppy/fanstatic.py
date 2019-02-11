from fanstatic import Library, Resource, Group, Inclusion
from js.jquery_form import jquery_form
from js.adminlte import adminlte_skin_blue_css
from js.adminlte import adminlte_js
from js.adminlte import all_plugins_js
from js.adminlte import pace_js, input_mask, bootstrap_wysihtml5_js, fontawesome_css

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
                     minifier='jsmin',
                     depends=[adminlte_js, fontawesome_css],
                     bottom=True)

edit_js = Resource(cuppylib,
                 'edit.js', 
                 minified='edit.min.js',
                 minifier = 'jsmin',
                 depends=[input_mask,pace_js, fontawesome_css, bootstrap_wysihtml5_js, adminlte_js, jquery_form],
                 bottom=True)

view_needed=Group([views_css, views_js])
edit_needed = Group([edit_css, edit_js])