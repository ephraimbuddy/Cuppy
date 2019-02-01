<%def name="render_field(field, **kwargs)">
%if field.type == "BooleanField":
<div class="form-group">
    ${field.label}
    <div class="checkbox">
        <label>${field}${field.label}
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
                ${subfield}
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
    ${field}
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