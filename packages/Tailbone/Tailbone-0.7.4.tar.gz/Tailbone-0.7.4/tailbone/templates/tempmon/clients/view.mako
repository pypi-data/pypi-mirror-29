## -*- coding: utf-8 -*-
<%inherit file="/master/view.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  <script type="text/javascript">
    $(function() {
        $('#restart-client').click(function() {
            $(this).button('disable').button('option', 'label', "Restarting, please wait...");
            location.href = '${url('tempmon.clients.restart', uuid=instance.uuid)}';
        });
    });
  </script>
</%def>

${parent.body()}

% if instance.enabled and master.restartable_client(instance) and request.has_perm('tempmon.clients.restart'):
    <div class="buttons">
      <button type="button" id="restart-client">Restart this Client</button>
    </div>
% endif
