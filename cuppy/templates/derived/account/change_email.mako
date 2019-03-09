<%inherit file="cuppy:templates/base/base.mako"/>
<div class="card">
    <div class="card-body">
<h4 class="card-title">Change Email</h4>
<p>Change your email address.</p>
<hr/>
    <div class="row">
    <div class="col-sm-6">
        <div id="feedback"></div>
    <form method="post"  id="ChangeEmail">
        ${form.csrf_token}
        %if form.csrf_token.errors:
            <div class="error">Invalid form submitted</div>
        %endif
       <div class="form-group">
                %for error in form.email.errors:
            <div class="error">${error}</div>
            %endfor
           <label>Change login Email</label>
                ${form.email(class_='form-control', placeholder="Email")}
            </div>

        <div class="form-group">
        <button type="submit" class="btn btn-primary">Update Email</button> </div>
    </form>
    </div>
    <div class="col-sm-6"></div></div>
</div>
</div>