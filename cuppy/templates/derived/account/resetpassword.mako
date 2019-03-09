<%inherit file="cuppy:templates/base/base.mako" />
  <div class="box box-default">
        <div class="box-header">
            <h3 class="box-title">Set a new password</h3>
        </div>
        <div class="box-body">
            <form action="${action_url}" method="post">
                        ${form.csrf_token}
                %if form.csrf_token.errors:
                    <div class="alert alert-danger">Your session has expired, refresh to continue</div>
                %endif
        		<div class="form-group">
                        %for error in form.password.errors:
                                <div class="text-danger">${error}</div>
                            %endfor
                            ${form.password(class_="form-control",placeholder="Password")}
                </div>
                <div class="form-group">
                        %for error in form.confirm_password.errors:
                                <div class="text-danger">${error}</div>
                            %endfor
                            ${form.confirm_password(class_="form-control",placeholder="Repeat Password")}
                </div>
                <div class="form-group">
                    <button type="submit" class="btn btn-primary px-2">Submit</button>
                </div>
            </form>
        </div>

  </div>