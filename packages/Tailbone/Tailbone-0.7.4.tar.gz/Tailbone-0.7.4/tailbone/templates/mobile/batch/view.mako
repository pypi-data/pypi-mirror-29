## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/view.mako" />

${parent.body()}

% if master.has_rows:
    % if master.mobile_rows_creatable and not batch.executed and not batch.complete:
        ${h.link_to("Add Item", url('mobile.{}.create_row'.format(route_prefix), uuid=instance.uuid), class_='ui-btn ui-corner-all')}
    % endif
    <br />
    ${grid.render_complete()|n}
% endif

% if not batch.executed:
    % if request.has_perm('{}.edit'.format(permission_prefix)):
        % if batch.complete:
            ${h.form(url('mobile.{}.mark_pending'.format(route_prefix), uuid=batch.uuid))}
            ${h.csrf_token(request)}
            ${h.hidden('mark-pending', value='true')}
            ${h.submit('submit', "Mark Batch as Pending")}
            ${h.end_form()}
        % else:
            ${h.form(url('mobile.{}.mark_complete'.format(route_prefix), uuid=batch.uuid))}
            ${h.csrf_token(request)}
            ${h.hidden('mark-complete', value='true')}
            ${h.submit('submit', "Mark Batch as Complete")}
            ${h.end_form()}
        % endif
    % endif
    % if batch.complete and master.mobile_executable and request.has_perm('{}.execute'.format(permission_prefix)):
        % if master.has_execution_options(batch):
            ${h.link_to("Execute Batch", url('mobile.{}.execute'.format(route_prefix), uuid=batch.uuid), class_='ui-btn ui-corner-all')}
        % else:
            ${h.form(url('mobile.{}.execute'.format(route_prefix), uuid=batch.uuid))}
            ${h.csrf_token(request)}
            ${h.submit('submit', "Execute Batch")}
            ${h.end_form()}
        % endif
    % endif
% endif
