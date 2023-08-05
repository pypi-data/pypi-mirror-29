## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if master.people_detachable and request.has_perm('{}.detach_person'.format(permission_prefix)):
      <script type="text/javascript">

        $(function() {
            $('.people .grid .actions a.detach').click(function() {
                if (! confirm("Are you sure you wish to detach this Person from the Customer?")) {
                    return false;
                }
            });
        });

      </script>
  % endif
</%def>

${parent.body()}
