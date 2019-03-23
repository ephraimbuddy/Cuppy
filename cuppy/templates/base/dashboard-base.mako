<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>${api.page_title}</title>
  <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
  <link rel="stylesheet" href="${request.static_url('cuppy:static/bootstrap/css/bootstrap.min.css')}">
  <link rel="stylesheet" href="${request.static_url('cuppy:static/adminlte/css/AdminLTE.min.css')}">
  <link rel="stylesheet" href="${request.static_url('cuppy:static/adminlte/css/skin-blue.min.css')}">
 <link rel="stylesheet" href="${request.static_url('cuppy:static/fontawesome/css/font-awesome.min.css')}">
 <link rel="stylesheet" href="${request.static_url('cuppy:static/bootstrap-wysihtml5/bootstrap3-wysihtml5.min.css')}">
  <%block name="header_tags"></%block>
  <!-- Google Font -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700,300italic,400italic,600italic">
  <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
</head>
<body class="hold-transition skin-blue sidebar-mini">
<div class="wrapper">

  <header class="main-header">
    <!-- Logo -->
    <a href="#" class="logo">
      <!-- mini logo for sidebar mini 50x50 pixels -->
      <span class="logo-mini"><b>A</b>LT</span>
      <!-- logo for regular state and mobile devices -->
      <span class="logo-lg"><b>Admin</b>LTE</span>
    </a>
    
    <nav class="navbar navbar-static-top">
      <!-- Sidebar toggle button-->
      <a href="#" class="sidebar-toggle" data-toggle="push-menu" role="button">
        <span class="sr-only">Toggle navigation</span>
      </a>

      <div class="navbar-custom-menu">
        <ul class="nav navbar-nav">
          
          <!-- User Account: -->
          <li class="dropdown user user-menu">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
              ##<img src="#" class="user-image" alt="User Image">
              <span class="hidden-xs">Alexander Pierce</span>
            </a>
            <ul class="dropdown-menu">
              <!-- User image -->
              <li class="user-header">
                <img src="" class="img-circle" alt="User Image">
                <p>
                  Alexander Pierce - Web Developer
                  <small>Member since Nov. 2012</small>
                </p>
              </li>
              
            </ul>
          </li>
          <!-- Control Sidebar Toggle Button -->
          <li>
            <a href="#" data-toggle="control-sidebar"><i class="fa fa-gears"></i></a>
          </li>
        </ul>
      </div>
    </nav>
  </header>
  <!-- Left side column. contains the logo and sidebar -->
  <aside class="main-sidebar">
    <!-- sidebar: style can be found in sidebar.less -->
    <section class="sidebar">
      <!-- Sidebar user panel -->
      <div class="user-panel">
        <div class="pull-left image">
          <img src="dist/img/user2-160x160.jpg" class="img-circle" alt="User Image">
        </div>
        <div class="pull-left info">
          <p>Alexander Pierce</p>
          <a href="#"><i class="fa fa-circle text-success"></i> Online</a>
        </div>
      </div>
      <!-- search form -->
      <form action="#" method="get" class="sidebar-form">
        <div class="input-group">
          <input type="text" name="q" class="form-control" placeholder="Search...">
          <span class="input-group-btn">
                <button type="submit" name="search" id="search-btn" class="btn btn-flat"><i class="fa fa-search"></i>
                </button>
              </span>
        </div>
      </form>
      <!-- /.search form -->
      <!-- sidebar menu: : style can be found in sidebar.less -->
      <ul class="sidebar-menu" data-widget="tree">
        <li class="header">Content</li>
            <li><a href="${request.route_url('page')}"><i class="fa fa-circle-o"></i><span> Pages</span></a></li>
        <li class="header">Users</li>
          <li><a href="${request.route_url('users')}"><i class="fa fa-circle-o"></i><span>users</span></a></li>
          
        
      </ul>
    </section>
    <!-- /.sidebar -->
  </aside>

  <!-- Content Wrapper. Contains page content -->
  <div class="content-wrapper">
   <%block name="content_header">
    <!-- Content Header (Page header) -->
    <section class="content-header">
      <h1>
        Dashboard
        <small>Control panel</small>
      </h1>
      <ol class="breadcrumb">
        <li class="active"><i class="fa fa-dashboard"></i> Home</li>
      </ol>
    </section>
      </%block>
    <!-- Main content -->
    <section class="content">
      ${next.body()}
    </section>
    <!-- /.content -->
  </div>
  <!-- /.content-wrapper -->
  <footer class="main-footer">
    <div class="pull-right hidden-xs">
    <%!
    import cuppy
    %>
      <b>Version</b> ${cuppy.get_version()}
    </div>
    <strong>Copyright &copy; 2019 <a href="#">Cuppy CMS</a>.</strong> All rights
    reserved.
  </footer>

  
 
</div>
<!-- ./wrapper -->

<script src="${request.static_url('cuppy:static/jquery/jquery.v3.3.1.min.js')}"></script>
<script src="${request.static_url('cuppy:static/bootstrap/js/bootstrap.min.js')}"></script>
<script src="${request.static_url('cuppy:static/adminlte/js/adminlte.min.js')}"></script>
<script src="${request.static_url('cuppy:static/jquery/fastclick.js')}"></script>
<script src="${request.static_url('cuppy:static/jquery/jquery.slimscroll.min.js')}"></script>
<script src="${request.static_url('cuppy:static/bootstrap-wysihtml5/bootstrap3-wysihtml5.all.min.js')}"></script>
<%block name="bottom_tags">
<script>
$(document).ready(function() {
     function getDateTime() {
    var now     = new Date(); 
    var year    = now.getFullYear();
    var month   = now.getMonth()+1; 
    var day     = now.getDate();
    var hour    = now.getHours();
    var minute  = now.getMinutes();
    var second  = now.getSeconds(); 
    if(month.toString().length == 1) {
         month = '0'+month;
    }
    if(day.toString().length == 1) {
         day = '0'+day;
    }   
    if(hour.toString().length == 1) {
         hour = '0'+hour;
    }
    if(minute.toString().length == 1) {
         minute = '0'+minute;
    }
    if(second.toString().length == 1) {
         second = '0'+second;
    }   
    var dateTime = year+'-'+month+'-'+day+' '+hour+':'+minute+':'+second;   
     return dateTime;
}
$("#now").click(function(){
    var datetime = new Date().toLocalString;
    $("#creation_date").val(getDateTime());
});
//bootstrap WYSIHTML5 - text editor
    $('#body').wysihtml5()
});
</script>
</%block>
</body>
</html>
