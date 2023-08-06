## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if not instance.users and request.has_perm('users.create'):
      <script type="text/javascript">
        $(function() {
            $('#make-user').click(function() {
                if (confirm("Really make a user account for this person?")) {
                    disable_button(this);
                    $('form[name="make-user-form"]').submit();
                }
            });
        });
      </script>
  % endif
</%def>

${parent.body()}

% if not instance.users and request.has_perm('users.create'):
    ${h.form(url('people.make_user'), name='make-user-form')}
    ${h.csrf_token(request)}
    ${h.hidden('person_uuid', value=instance.uuid)}
    ${h.end_form()}
% endif
