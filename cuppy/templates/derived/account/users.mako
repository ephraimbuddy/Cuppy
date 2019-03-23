<%inherit file="cuppy:templates/base/dashboard-base.mako"/>

<%block name="content_header">
<!-- Content Header (Page header) -->
    <section class="content-header">
      <h1>
        Dashboard
        <small>Users</small>
      </h1>
      <ol class="breadcrumb">
        <li><a href="${request.route_url('dashboard')}"><i class="fa fa-dashboard"></i> Home</a></li>
        <li class="active">users</li>
      </ol>
      </section>
</%block>
<div class="box box-primary">
    <div class="box-header with-border">
    ##<a href="" class="btn btn-primary pull-right">Add User</a>
    </div>
    <div class="box-body ">
    <div class="row">
        <div class="col-lg-9 col-md-12">
            <div class="table-responsive ">
            <table class="table table-condensed table-bordered">
                <tbody>
    <tr>
    <th>Username</th>
    <th>Email</th>
    <th>Firstname</th>
    <th>Lastname</th>
    <th>Date Joined</th>
    <th>Last Login</th>
    <th>Permission Group</th>
</tr>
%if users:
    %for user in users:
    <tr>
        <td><a href="${request.route_url('admin_edit_user', id=user.id)}">${user.username}</a></td>
        <td>${user.email}</td>
        <td>${user.first_name}</td>
        <td>${user.last_name}</td>
        <td></td>
        <td>${user.last_login}</td>
        <td>${user.mygroups}</td>
    <tr>
    %endfor
%endif
    </tbody>
    </table>
</div>
    <div class="col-lg-3 col-md-12"></div>
</div>
</div>