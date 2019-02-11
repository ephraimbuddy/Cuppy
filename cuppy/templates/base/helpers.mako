<%def name="render_field(field, **kwargs)">
%if field.type == "BooleanField":
<div class="form-group">
    ${field.label}
    <div class="checkbox">
        <label>${field(**kwargs)}${field.label}
        </label>
    </div>
    %if field.flags.required:
        <span class="text-danger">*</span>
    %endif
    <div class="help-block">${field.description}</div>
    %if field.errors:
        <ul class="errors list-unstyled">
            %for error in field.errors:
                <li class="text-danger">${error }</li>
            %endfor 
        </ul>
    %endif
</div>


%elif field.type == "RadioField":
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
});
</script>
    ${field.label}
    ${field(**kwargs)}
    <button type="cancel" id="now" class="btn btn-primary btn-xs">Now</button>
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
<div class="box box-default collapsed-box box-solid">
            <div class="box-header with-border">
              <h3 class="box-title">
              <a href="${request.route_url('edit_doc', slug=page.get_slug())}">${page.title}</a></h3>

              <div class="box-tools pull-right">
              
              <select class="add_docs">
                <option>Add ...</option>
                <option value="${request.route_path('add_doc',parent_id=page.id)}">Add page</option>
                </select>
                <button type="button" class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-plus"></i>
                </button>
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