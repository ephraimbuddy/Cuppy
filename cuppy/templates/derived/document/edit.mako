<%inherit file="cuppy:templates/base/dashboard-base.mako"/>
<%namespace name="field" file="cuppy:templates/derived/document/fields.mako"/>

<div class="box box-primary">
<div class="box-header with-body">
<h3 class="box-title">Edit ${doc.title}</h3>

${field.doc_form(form)}


</div>
</div>
