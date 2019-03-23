<%inherit file="cuppy:templates/base/dashboard-base.mako"/>
<%namespace name="helper" file="cuppy:templates/base/helpers.mako"/>

<%block name="content_header">
<!-- Content Header (Page header) -->
    <section class="content-header">
      <h1>
        Dashboard
        <small>Edit User</small>
      </h1>
      <ol class="breadcrumb">
        <li><a href="${request.route_url('dashboard')}"><i class="fa fa-dashboard"></i> Home</a></li>
        <li><a href="${request.route_url('users')}"> users</a></li>
        <li class="active">edit user</li>
      </ol>
      </section>
</%block>
<div class='row'>
    <div class="col-lg-6 col-md-12">
<div class="box box-primary">
    <div class="box-header with-border">
    <h1>Change user</h1>
        </div>
        <form method="post">
    <div class="box-body">
    
        ${form.csrf_token()}
${helper.render_field(form.username, class_="form-control")}
<div class="form-group">
    <label>Password</label>
    <p class="help-block">Passwords are encrypted, you cannot change it here</p>
</div>
${helper.render_field(form.first_name, class_="form-control")}
${helper.render_field(form.last_name, class_="form-control")}
${helper.render_field(form.email, class_="form-control")}
${helper.render_field(form.about, class_="form-control", rows='6')}
    </div>
    <div class="box-footer">
    <button type="submit" class="btn btn-primary pull-right">Save</button>
    </div>
</form>
</div>
    </div><!-- End col-->
    <div class="col-lg-6 col-md-12">
<div class="box box-primary">
    <div class="box-header with-border">
        <h1>Permission group</h1>
        </div>
    <div class="box-body">
    <p>This user belongs to the following groups: <code>${user.mygroups}</code>
    <div class="table-responsive ">
            <table class="table table-condensed table-bordered">
                <tbody>
                    
                %if groups:
                %for group in groups:
                <tr>
                <td>
                    <a href="${request.route_url('add_to_group', user_id=user.id,name=group.name)}" class="btn btn-primary">Add user to group ${group.name}</a>
                    <a href="${request.route_url('remove_from_group', user_id=user.id,name=group.name)}" class="btn btn-danger">Remove user from group ${group.name}</a>
                </td>
                </tr>
                %endfor
                %endif
                </tbody>
                </table>
    </div>

    </div>
</div>
    </div>
</div><!-- End row -->