## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">
    $(function() {

        $('form[name="restart-datasync"]').submit(function() {
            $(this).find('button')
                .button('option', 'label', "Restarting DataSync...")
                .button('disable');
        });

    });
  </script>
</%def>

<%def name="grid_tools()">
  ${parent.grid_tools()}
  ${h.form(url('datasync.restart'), name='restart-datasync')}
  ${h.csrf_token(request)}
  <button type="submit">Restart DataSync</button>
  ${h.end_form()}
</%def>

${parent.body()}
