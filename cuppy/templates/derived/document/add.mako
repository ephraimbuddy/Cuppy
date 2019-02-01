<%inherit file="cuppy:templates/base/dashboard-base.mako"/>
<%namespace name="helper" file="cuppy:templates/base/helpers.mako"/>

<div class="box box-primary">
<div class="box-header with-body">
<h3 class="box-title">Add a document</h3>

<form action="${request.route_url('add_doc')}" method="post">
<div class="box-body">
${form.csrf_token()}
${helper.render_field(form.title, class_="form-control")}
${helper.render_field(form.status)}
${helper.render_field(form.creation_date, class_="form-control")}
${helper.render_field(form.in_menu)}
${helper.render_field(form.body, class_="form-control", rows=5)}
${helper.render_field(form.meta_title, class_="form-control")}
${helper.render_field(form.description, class_="form-control", rows=3)}
${helper.render_field(form.slug, class_="form-control")}

<div class="box-footer">
    <button type="submit" class="btn btn-primary">Submit</button>
</div>
</div>
</form>

</div>
</div>