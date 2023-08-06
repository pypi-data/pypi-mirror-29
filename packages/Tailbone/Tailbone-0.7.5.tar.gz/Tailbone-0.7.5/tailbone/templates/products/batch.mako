## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">Products: Create Batch</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Back to Products", url('products'))}</li>
</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">
    $(function() {

        $('select[name="batch_type"]').on('selectmenuchange', function(event, ui) {
            $('.params-wrapper').hide();
            $('.params-wrapper.' + ui.item.value).show();
        });

        $('.params-wrapper.' + $('select[name="batch_type"]').val()).show();

    });
  </script>
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">
    .params-wrapper {
        display: none;
    }
  </style>
</%def>

<%def name="render_deform_field(field)">
  <div class="field-wrapper ${field.name}">
    <div class="field-row">
      <label for="${field.oid}">${field.title}</label>
      <div class="field">
        ${field.serialize()|n}
      </div>
    </div>
  </div>
</%def>


<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form">
  ${h.form(request.current_route_url(), class_='autodisable')}
  ${h.csrf_token(request)}

  ${render_deform_field(dform['batch_type'])}
  ${render_deform_field(dform['description'])}
  ${render_deform_field(dform['notes'])}

  % for key, pform in params_forms.items():
      <div class="params-wrapper ${key}">
        ## TODO: hacky to use deform? at least is explicit..
        % for field in pform.make_deform_form():
            ${render_deform_field(field)}
        % endfor
      </div>
  % endfor

  <div class="buttons">
    ${h.submit('make-batch', "Create Batch")}
    ${h.link_to("Cancel", url('products'), class_='button')}
  </div>

  ${h.end_form()}
</div>
