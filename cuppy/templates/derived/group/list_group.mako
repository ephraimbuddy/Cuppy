<%inherit file="cuppy:templates/base/dashboard-base.mako"/>
<%namespace file="cuppy:templates/base/helpers.mako" import="simple_modal"/>
<div class="row">
    <div class="col-lg-6 col-md-12">
<div class="box box-primary">
<div class="box-header with-body">
<h3 class="box-title">Permission Groups</h3>
<a href="${request.route_url('add_group')}" class="btn btn-primary pull-right">Add New Group</a>
</div>
<div class="box-body table-responsive ">
<table class="table table-condensed">
<tbody>
<tr>
    <th>Name</th>
    <th>Actions</th>
</tr>
%if groups:

%for g in groups:
<tr>
    <td><a href="${request.route_url('edit_group', id=g.id)}">${g.name}</a></td>
    <td>
    <a href="#" onclick="$('#delete-modal a').attr('href', '${request.route_url('delete_group', id=g.id)}');" data-toggle="modal" data-target="#delete-modal" class="btn btn-danger btn-sm">Delete</a>
    </td>
</tr>
%endfor
%else:
<tr><td>
<p class="text-center">No group available</p>
</td></tr>
%endif
    </tbody>
</table>
</div>
</div>
    </div>
</div>

${simple_modal("Delete Group", "Do you want to delete this permission group? Action cannot be undone")}