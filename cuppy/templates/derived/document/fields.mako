<%namespace name="helper" file="cuppy:templates/base/helpers.mako"/>


<%def name="doc_form(form)">
<form action="${action_url}" method="post">
<div class="box-body">
${form.csrf_token()}
${helper.render_field(form.title, class_="form-control")}
${helper.render_field(form.status)}
${helper.render_field(form.creation_date)}
${helper.render_field(form.in_menu)}
${helper.render_field(form.body, class_="form-control", rows=15)}
${helper.render_field(form.tags, class_="form-control")}
    <div class="box box-default collapsed-box box-solid">
            <div class="box-header with-border">
              <h3 class="box-title">meta</h3>
              <div class="box-tools pull-right">
                <button type="button" class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-plus"></i>
                </button>
              </div>
              </div>
              <div class="box-body">
${helper.render_field(form.meta_title, class_="form-control")}
${helper.render_field(form.description, class_="form-control", rows=3)}
${helper.render_field(form.slug, class_="form-control")}

              </div>
    </div>
<div class="box-footer">
    <button type="submit" class="btn btn-primary">Submit</button>
</div>
</div>
</form>
</%def>