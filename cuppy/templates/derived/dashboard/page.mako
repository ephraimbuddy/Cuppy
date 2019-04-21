<%inherit file="cuppy:templates/base/dashboard-base.mako"/>
<%namespace file="cuppy:templates/base/helpers.mako" import="render_pages, simple_modal"/>

<%block name="content_header">
<!-- Content Header (Page header) -->
    <section class="content-header">
      <h1>
        Dashboard
        <small>Pages</small>
      </h1>
      <ol class="breadcrumb">
        <li><a href="${request.route_url('dashboard')}"><i class="fa fa-dashboard"></i> Home</a></li>
        <li class="active">pages</li>
      </ol>
      </section>
</%block>

<div class="row">
    <div class="col-lg-9 col-md-12">
<div class="box box-primary">
    <div class="box-header">
    <i class="fa fa-folder"></i>
    <div class="box-title">Select Page to change</div>
    <div class="pull-right">
    <select class="add_docs">
                <option>Add ...</option>
                %for ilist in api.page_add_options:
                    %for item in ilist:
                <option value="${request.route_url(item[0])}">${item[1]}</option>
                    %endfor
                %endfor
                </select>
                </div>
    </div>
    <div class="box-body">
    <ul class="list-unstyled">
    
    %for page in docs:
    ${render_pages(page)}
    %endfor
    </ul>
    
    </div>
    <div class="box-footer">
    </div>
</div>
    </div> <!-- End col-lg-6 col-md-12 -->
    <div class="col-lg-3 col-md-12">
    </div>
</div>


${simple_modal("Delete Page", "Do you really want to delete this page?")}