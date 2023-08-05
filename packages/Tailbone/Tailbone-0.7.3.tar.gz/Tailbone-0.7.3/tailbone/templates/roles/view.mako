## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_styles()">
  ${parent.extra_styles()}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/perms.css'))}
</%def>

${parent.body()}

<h2>Users</h2>

% if instance is guest_role:
    <p>The guest role is implied for all anonymous users, i.e. when not logged in.</p>
% elif instance is authenticated_role:
    <p>The authenticated role is implied for all users, but only when logged in.</p>
% elif users:
    <p>The following users are assigned to this role:</p>
    ${users.render_grid()|n}
% else:
    <p>There are no users assigned to this role.</p>
% endif
