## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.batch.js') + '?ver={}'.format(tailbone.__version__))}
  <script type="text/javascript">

    var has_execution_options = ${'true' if master.has_execution_options(batch) else 'false'};

    $(function() {
        % if master.has_worksheet:
            $('.load-worksheet').click(function() {
                $(this).button('disable').button('option', 'label', "Working, please wait...");
                location.href = '${url('{}.worksheet'.format(route_prefix), uuid=batch.uuid)}';
            });
        % endif
        % if master.batch_refreshable(batch) and request.has_perm('{}.refresh'.format(permission_prefix)):
            $('#refresh-data').click(function() {
                $(this)
                    .button('option', 'disabled', true)
                    .button('option', 'label', "Working, please wait...");
                location.href = '${url('{}.refresh'.format(route_prefix), uuid=batch.uuid)}';
            });
        % endif
    });

  </script>
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">

    .grid-wrapper {
        margin-top: 10px;
    }
    
  </style>
</%def>

<%def name="buttons()">
    <div class="buttons">
      ${self.leading_buttons()}
      ${refresh_button()}
      ${execute_button()}
    </div>
</%def>

<%def name="leading_buttons()">
  % if master.has_worksheet and master.allow_worksheet(batch) and request.has_perm('{}.worksheet'.format(permission_prefix)):
      <button type="button" class="load-worksheet">Edit as Worksheet</button>
  % endif
</%def>

<%def name="refresh_button()">
  % if master.viewing and master.batch_refreshable(batch) and request.has_perm('{}.refresh'.format(permission_prefix)):
      <button type="button" id="refresh-data">Refresh Data</button>
  % endif
</%def>

<%def name="execute_button()">
  % if not batch.executed and request.has_perm('{}.execute'.format(permission_prefix)):
      <button type="button" id="execute-batch"${'' if execute_enabled else ' disabled="disabled"'}>${execute_title}</button>
  % endif
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
  ${form.render(form_id='batch-form', buttons=capture(buttons))|n}
</div><!-- form-wrapper -->

${rows_grid|n}

% if not batch.executed:
    <div id="execution-options-dialog" style="display: none;">
      ${execute_form.render_deform(form_kwargs={'name': 'batch-execution'}, buttons=False)|n}
    </div>
% endif
