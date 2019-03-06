<%inherit file="cuppy:templates/base/dashboard-base.mako"/>
<%namespace file="cuppy:templates/base/helpers.mako" import="render_pages, simple_modal"/>
<%block name="bottom_tags">
${parent.bottom_tags}
        <script>
              jQuery(function($) {
    $('.add_docs').change(function() {
        var addUrl = this[this.selectedIndex].value;
        //console.log(addUrl);
        // If the browser's back button is hit from the add interface,
        // the browser may maintain the state of the select list in the
        // list interface, in which case the previously selected option
        // will still be selected. This would mean the first option
        // (eg "Add ..."") could be selected, which contains no URL to
        // redirect to, so we guard against that, also set selectedIndex
        // back to zero, to also protect against this scenario.
        if (addUrl) {
            location.href = addUrl;
            this.selectedIndex = 0;
        }
    });
});
              </script>
              </%block>
<div class="row">
    <div class="col-lg-9 col-md-12">
<div class="box box-primary">
    <div class="box-header">
    <i class="fa fa-folder"></i>
    <div class="box-title">Select Page to change</div>
    <div class="pull-right">
    <select class="add_docs">
                <option>Add ...</option>
                <option value="${request.route_path('add_doc')}">Add page</option>
                </select>
                </div>
    </div>
    <div class="box-body">
    <ul class="list-unstyled">
    
    %for page in docs:
    ${render_pages(page)}
    %endfor
    </ul>
    
    </div>
    <div class="box-footer">
    </div>
</div>
    </div> <!-- End col-lg-6 col-md-12 -->
    <div class="col-lg-3 col-md-12">
    </div>
</div>


${simple_modal("Delete Page", "Do you really want to delete this page?")}