<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
  
    <meta name="keywords" content="${api.meta_keywords}">
    
    <meta name="description" content="${api.meta_description}">
    
    <title>Signin - ${api.page_title}</title>

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
  <body class="hold-transition login-page">
<div class="login-box">
  <div class="login-logo">
    <a href="/">${api.page_title}</a>
  </div>
  <!-- /.login-logo -->
  <div class="login-box-body">
    <p class="login-box-msg">Sign in</p>

    <form action="${action_url}" method="post">
    ${form.csrf_token}
        %if form.csrf_token.errors:
        <div class="red">You have submitted an invalid form, please refresh page and try again</div>
        %endif
        <p style="color:red">${message}</p>
        <input type="hidden" name="came_from" value=${came_from} />
      <div class="form-group has-feedback">
      %for error in form.email.errors:
            <div class="error">${error}</div>
            %endfor
        ${form.email(class_='form-control required', placeholder="Email")}
        <span class="glyphicon glyphicon-envelope form-control-feedback"></span>
      </div>
      
      <div class="form-group has-feedback">
      %for error in form.password.errors:
            <div class="error">${error}</div>
            %endfor
        ${form.password(class_='form-control required', placeholder="Password")}
        <span class="glyphicon glyphicon-lock form-control-feedback"></span>
      </div>
      <div class="row">
       
        <!-- /.col -->
        <div class="col-xs-12">
          <button type="submit" class="btn btn-primary btn-block btn-flat">Sign In</button>
        </div>
        <!-- /.col -->
      </div>
    </form>

    <a href="#">I forgot my password</a><br>
    <a href="${request.route_url('signup')}" class="text-center">Register a new user</a>

  </div>
  <!-- /.login-box-body -->
</div>
<!-- /.login-box -->
<script src="${request.static_url('cuppy:static/jquery/jquery.v3.3.1.min.js')}"></script>
<script src="${request.static_url('cuppy:static/bootstrap/js/bootstrap.min.js')}"></script>
<script src="${request.static_url('cuppy:static/adminlte/js/adminlte.min.js')}"></script>

  </body>
</html>