## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">Find ${model_title_plural} by Permission</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">

    <% gcount = len(permissions) %>
    var permissions_by_group = {
    % for g, (gkey, group) in enumerate(permissions, 1):
        <% pcount = len(group['perms']) %>
        '${gkey}': {
        % for p, (pkey, perm) in enumerate(group['perms'], 1):
            '${pkey}': "${perm['label']}"${',' if p < pcount else ''}
        % endfor
        }${',' if g < gcount else ''}
    % endfor
    };

    $(function() {

        $('#permission_group').selectmenu({
            change: function(event, ui) {
                var perms = $('#permission');
                perms.find('option:first').siblings('option').remove();
                $.each(permissions_by_group[ui.item.value], function(key, label) {
                    perms.append($('<option value="' + key + '">' + label + '</option>'));
                });
                perms.selectmenu('refresh');
            }
        });

        $('#permission').selectmenu();

        $('#find-by-perm-form').submit(function() {
            $('.grid').remove();
            $(this).find('#submit').button('disable').button('option', 'label', "Searching, please wait...");
        });

    });

  </script>
</%def>


${h.form(request.current_route_url(), id='find-by-perm-form')}
${h.csrf_token(request)}

<div class="form">
  ${self.wtfield(form, 'permission_group')}
  ${self.wtfield(form, 'permission')}
  <div class="buttons">
    ${h.submit('submit', "Find {}".format(model_title_plural))}
  </div>
</div>

${h.end_form()}

% if principals is not None:
<div class="grid half">
  <br />
  <h2>${model_title_plural} with that permission (${len(principals)} total):</h2>
  ${self.principal_table()}
</div>
% endif
