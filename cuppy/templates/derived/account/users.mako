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