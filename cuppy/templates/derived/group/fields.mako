<%namespace name="helper" file="cuppy:templates/base/helpers.mako"/>

<%def name="group_form(form)">
<form action="${action_url}" method="post">
<div class="box-body">
${form.csrf_token()}
${helper.render_field(form.name, class_="form-control")}
</div>
<div class="box-footer">
    <button type="cancel" class="btn btn-default">cancel</button>
    <button type="submit" class="btn btn-primary pull-right">Submit</button>
</div>
</div>
</form>
</%def>
