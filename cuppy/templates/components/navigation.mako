<nav class="navbar navbar-default">
  <div class="container">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="/">${api.site_title}</a>
    </div>
    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
      <li class="${api.home and 'active'}"><a href="/">Home</a></li>
    %if contents:
    
      %for content in contents:
        %if not content.children:
            <li class="${api.current_page(content) and 'active'}"><a href="${request.route_url('view_doc',slug=content.slug)}">${content.title}</a></li>
        %else:
            <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">${content.title} <span class="caret"></span></a>
          <ul class="dropdown-menu">
            %for child in content.children:
            
            <li class="${api.current_page(child) and 'active'}"><a href="${request.route_url('view_doc',slug=child.slug)}">${child.title}</a></li>
            %endfor
          </ul>
        </li>
        %endif
      %endfor
      
    %endif
    </ul>
    <ul class="nav navbar-nav navbar-right">
    %if request.user:
    <li><a href="${request.route_url('dashboard')}" class="navbar-link">Dashboard</a></li>
    <li><a href="${request.route_url('signout')}" class="navbar-link">Signout</a></li>
    %else:
    <li><a href="${request.route_url('signin')}" class="navbar-link">Signin</a></li>
    <p class="navbar-text">or</p>
    <li><a href="${request.route_url('signup')}" class="navbar-link">Signup</a></li>
    %endif
    </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>