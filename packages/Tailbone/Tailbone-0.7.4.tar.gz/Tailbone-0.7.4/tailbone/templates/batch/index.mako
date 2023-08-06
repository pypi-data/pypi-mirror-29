## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if master.results_executable and request.has_perm('{}.execute_multiple'.format(permission_prefix)):
      <script type="text/javascript">

        var has_execution_options = ${'true' if master.has_execution_options(batch) else 'false'};
        var dialog_opened = false;

        $(function() {

            $('#execute-results-button').click(function() {
                var count = $('.grid-wrapper').gridwrapper('results_count');
                if (!count) {
                    alert("There are no batch results to execute.");
                    return;
                }
                var form = $('form[name="execute-results"]');
                if (has_execution_options) {
                    $('#execution-options-dialog').dialog({
                        title: "Execution Options",
                        width: 550,
                        height: 300,
                        modal: true,
                        buttons: [
                            {
                                text: "Execute",
                                click: function(event) {
                                    dialog_button(event).button('option', 'label', "Executing, please wait...").button('disable');
                                    form.submit();
                                }
                            },
                            {
                                text: "Cancel",
                                click: function() {
                                    $(this).dialog('close');
                                }
                            }
                        ],
                        open: function() {
                            if (! dialog_opened) {
                                $('#execution-options-dialog select[auto-enhance="true"]').selectmenu();
                                $('#execution-options-dialog select[auto-enhance="true"]').on('selectmenuopen', function(event, ui) {
                                    show_all_options($(this));
                                });
                                dialog_opened = true;
                            }
                        }
                    });
                } else {
                    $(this).button('option', 'label', "Executing, please wait...").button('disable');
                    form.submit();
                }
            });

        });

      </script>
  % endif
</%def>

<%def name="grid_tools()">
  % if master.results_executable and request.has_perm('{}.execute_multiple'.format(permission_prefix)):
      <button type="button" id="execute-results-button">Execute Results</button>
  % endif
</%def>

${parent.body()}

% if master.results_executable and request.has_perm('{}.execute_multiple'.format(permission_prefix)):
    <div id="execution-options-dialog" style="display: none;">
      <br />
      <p>
        Please be advised, you are about to execute multiple batches!
      </p>
      <br />
      ${execute_form.render_deform(form_kwargs={'name': 'execute-results'}, buttons=False)|n}
    </div>
% endif
