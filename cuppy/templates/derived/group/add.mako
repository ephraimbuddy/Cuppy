<%inherit file="cuppy:templates/base/dashboard-base.mako"/>
<%namespace name="field" file="cuppy:templates/derived/group/fields.mako"/>
<div class="row">
    <div class="col-lg-6 col-md-12">
<div class="box box-primary">
<div class="box-header with-body">
<h3 class="box-title">Add Group</h3>

${field.group_form(form)}


</div>
</div>
    </div>
</div>