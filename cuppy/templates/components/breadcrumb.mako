<ol class="breadcrumb">

%if breadcrumbs:
    <li><a href="${request.route_url('home')}">Home</a></li>
    %for c in breadcrumbs:
    %if api.current_page(c):
  <li class="active">${c.title}</li>
  %else:
  <li><a href="${request.route_url('view_doc',slug=c.get_slug())}">${c.title}</a></li>
  %endif
    %endfor
%else:
<li>Home</li>
%endif
</ol>
