<%inherit file="cuppy:templates/base/base.mako"/>
<div class="ibox">
    <h4 class="ibox-title">Change Password</h4>
    <div class="ibox-content">
<p>Change your Password.</p>
<hr/>
    <div class="row">
    <div class="col-sm-6">
        <div id="feedback"></div>
    <form method="post" id="ChangePassword">
        ${form.csrf_token}
        %if form.csrf_token.errors:
            <div class="error">Invalid form submitted</div>
        %endif
       <div class="form-group">
                    %for error in form.old_password.errors:
            <div class="error">${error}</div>
            %endfor
           <label>Old Password</label>
            ${form.old_password(class_='form-control')}
            </div>
        <div class="form-group">
                    %for error in form.password.errors:
            <div class="error">${error}</div>
            %endfor
             <label>New Password</label>
                  ${form.password(class_='form-control')}
               </div>
            <div class="form-group">
                %for error in form.confirm.errors:
            <div class="error">${error}</div>
            %endfor
                <label>Repeat Password</label>
                  ${form.confirm(class_='form-control')}
            </div>
        <div class="form-group">
        <button type="submit" class="btn btn-primary">Update Password</button> </div>
    </form>
    </div>
    <div class="col-sm-6"></div></div>
</div>
</div>