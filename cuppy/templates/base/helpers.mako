<%def name="render_field(field, **kwargs)">
%if field.type == "RadioField":
<div class="form-group">
        ${field.label}
    <div class="radio">
        %for subfield in field:
            <label class="radio-inline">
                ${subfield(**kwargs)}
                ${subfield.label}
            </label>
        %endfor
    </div>
    %if field.errors:
        <ul class="errors list-unstyled">
            %for error in field.errors:
                <li class="text-danger">${error }</li>
            %endfor 
        </ul>
    %endif
</div>
%elif field.type == "DateTimeField":
<div class="form-group">

    ${field.label}
    ${field(**kwargs)}
    <a href="#" id="now" class="btn btn-primary btn-xs">Now</a>
    <div class="help-block">${field.description}</div>
    %if field.errors:
        <ul class="errors list-unstyled">
            %for error in field.errors:
                <li class="text-danger">${error }</li>
            %endfor 
        </ul>
    %endif
</div>

%else:
<div class="form-group">
        ${field.label}
    %if field.flags.required:
        <span class="text-danger">*</span>
    %endif
        ${field(**kwargs)}
    <div class="help-block">${field.description}</div>
    %if field.errors:
        <ul class="errors list-unstyled">
            %for error in field.errors:
                <li class="text-danger">${error }</li>
            %endfor 
        </ul>
    %endif
</div>
%endif
</%def>

## Rendering of pages
<%def name="render_pages(page)">
<li>
<div class="box box-default box-solid">
            <div class="box-header with-border">
            <button type="button" class="btn btn-sm btn-box-tool" ><i class="fa fa-bars"></i>
                </button>
              <h3 class="box-title">
              <a href="${request.route_url(page.edit_route_name, slug=page.slug)}">${page.title}</a></h3>

              <div class="box-tools pull-right">
              
              <select class="add_docs">
                <option>Add ...</option>
                <option value="${request.route_path(page.add_route_name,parent_id=page.id)}">Add ${page.verbose_name}</option>
                </select>
                <button type="button" class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-minus"></i>
                </button>
                <a href="#" onclick="$('#delete-modal a').attr('href', '${request.route_url(page.delete_route_name, slug=page.slug)}');" data-toggle="modal" data-target="#delete-modal" class="btn btn-box-tool" ><i class="fa fa-trash"></i></a>
              </div>
              <!-- /.box-tools -->
            </div>
            %if page.children:
            <div class="box-body">
            <ul class="list-unstyled">
            %for i in page.children:
            <li>${render_pages(i)}</li>
            %endfor
            </ul>
            </div>
            %endif
</div>
</li>
</%def>

<%def name="simple_modal(title,body, button='Delete')">
<div class="modal modal-info fade" tabindex="-1" role="dialog" id="delete-modal">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">${title}</h4>
      </div>
      <div class="modal-body">
       ${body}
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default pull-left" data-dismiss="modal">Close</button>
        <a href="" class="btn btn-danger">${button}</a>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
</%def>