<%inherit file="cuppy:templates/base/base.mako"/>

    <div class="box box-default">
        <div class="box-header">
            <h3 class="box-title">Password Reset</h3>
            <p>Enter your email below</p>
        </div>
        <div class="box-body">
          <div id="feedback"></div> 
            <form action="${request.route_url('forgot_password')}" id="forgotPassword"  method="post">

                ${form.csrf_token}
                %if form.csrf_token.errors:
                    <div class="red">Refresh and try again</div>
                %endif
                <div class="form-group">
                %for error in form.email.errors:
                <div class="error">${error}</div>
                %endfor
                ${form.email(class_='form-control required', id="email", placeholder="Email")}
                </div>
                <div class="form-group">
                <button type="submit" id="forgotBtn" class="btn btn-warning btn-right">Reset Password</button>
                    </div>
            </form>
        </div>
    </div>
    
    