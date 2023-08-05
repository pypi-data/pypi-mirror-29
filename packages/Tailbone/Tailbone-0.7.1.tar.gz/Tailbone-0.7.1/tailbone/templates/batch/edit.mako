## -*- coding: utf-8; -*-
<%inherit file="/master/edit.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.batch.js'))}
  <script type="text/javascript">

    var has_execution_options = ${'true' if master.has_execution_options(batch) else 'false'};

    $(function() {

        $('#save-refresh').click(function() {
            var form = $(this).parents('form');
            form.append($('<input type="hidden" name="refresh" value="true" />'));
            form.submit();
        });

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
      % if master.refreshable:
          ${h.submit('save-refresh', "Save & Refresh Data")}
      % endif
      % if not batch.executed and request.has_perm('{}.execute'.format(permission_prefix)):
          <button type="button" id="execute-batch"${'' if execute_enabled else ' disabled="disabled"'}>${execute_title}</button>
      % endif
    </div>
</%def>

<%def name="grid_tools()">
    % if not batch.executed:
        <p>${h.link_to("Delete all rows matching current search", url('{}.delete_rows'.format(route_prefix), uuid=batch.uuid))}</p>
    % endif
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
  ${form.render()|n}
</div>

<div id="execution-options-dialog" style="display: none;">

  ${h.form(url('{}.execute'.format(route_prefix), uuid=batch.uuid), name='batch-execution')}
  % if master.has_execution_options(batch):
      ${rendered_execution_options|n}
  % endif
  ${h.end_form()}

</div>
