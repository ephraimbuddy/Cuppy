<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
  
    <meta name="keywords" content="${api.meta_keywords}">
    
    <meta name="description" content="${api.meta_description}">
    
    <title>Signup - ${api.page_title}</title>

  <link rel="stylesheet" href="${request.static_url('cuppy:static/bootstrap/css/bootstrap.min.css')}">
  <link rel="stylesheet" href="${request.static_url('cuppy:static/adminlte/css/AdminLTE.min.css')}">
  <link rel="stylesheet" href="${request.static_url('cuppy:static/adminlte/css/skin-blue.min.css')}">
 <link rel="stylesheet" href="${request.static_url('cuppy:static/fontawesome/css/font-awesome.min.css')}">
  
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body class="hold-transition register-page">
<div class="register-box">
  <div class="register-logo">
    <a href="/"><b>${api.page_title}</a>
  </div>

  <div class="register-box-body">
    <p class="login-box-msg">Register a new user</p>

    <form action="${action_url}" method="post">
     ${form.csrf_token}
            %if form.csrf_token.errors:
                <div class="text-danger">You have submitted an invalid form</div>
            %endif
      <div class="form-group has-feedback">
      <label>Firstname<span class="text-danger">*</span></label>
        %for error in form.first_name.errors:
            <div class="error">${error}</div>
            %endfor
            
            ${form.first_name(class_='form-control required', placeholder="First name")}
                    
        <span class="glyphicon glyphicon-user form-control-feedback"></span>
      </div>
      <div class="form-group has-feedback">
      <label>Lastname<span class="text-danger">*</span></label>
        %for error in form.last_name.errors:
            <div class="error">${error}</div>
            %endfor
            
            ${form.last_name(class_='form-control required', placeholder="Last name")}
                    
        <span class="glyphicon glyphicon-user form-control-feedback"></span>
      </div>
       <div class="form-group has-feedback">
       <label>Email<span class="text-danger">*</span></label>
        %for error in form.email.errors:
            <div class="error">${error}</div>
            %endfor
            
                ${form.email(class_='form-control required', placeholder="Email")}
        <span class="glyphicon glyphicon-envelope form-control-feedback"></span>
      </div>
      <div class="form-group has-feedback">
      <label>Username</label>
        %for error in form.username.errors:
            <div class="error">${error}</div>
            %endfor
                ${form.username(class_='form-control', placeholder="Username")}
        <span class="glyphicon glyphicon-user form-control-feedback"></span>
        <small class="help-block"> Only use letters, numbers, dashes or underscores</small>
      </div>
     
    
      <div class="form-group has-feedback">
      <label>Password<span class="text-danger">*</span></label>
        %for error in form.password.errors:
            <div class="error">${error}</div>
            %endfor
            
                ${form.password(class_='form-control required', placeholder="Password")}
        <span class="glyphicon glyphicon-lock form-control-feedback"></span>
      </div>
      <div class="form-group has-feedback">
      <label>Repeat Password<span class="text-danger">*</span></label>
        %for error in form.confirm.errors:
            <div class="error">${error}</div>
            %endfor
           
                ${form.confirm(class_='form-control required', placeholder="Repeat Password")}
        <span class="glyphicon glyphicon-log-in form-control-feedback"></span>
      </div>
      <div class="row">
        
        <!-- /.col -->
        <div class="col-xs-12">
          <button type="submit" class="btn btn-primary btn-block btn-flat">Register</button>
        </div>
        <!-- /.col -->
      </div>
    </form>

    <p><a href="${request.route_url('signin')}" class="text-center">I already have an account</a></p>
  </div>
  <!-- /.form-box -->
</div>
<!-- /.register-box -->
<script src="${request.static_url('cuppy:static/jquery/jquery.v3.3.1.min.js')}"></script>
<script src="${request.static_url('cuppy:static/bootstrap/js/bootstrap.min.js')}"></script>
<script src="${request.static_url('cuppy:static/adminlte/js/adminlte.min.js')}"></script>

  </body>
</html>