## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">Edit: ${instance_title}</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">

    $(function() {

        $('form').submit(function() {
            var submit = $(this).find('input[type="submit"]');
            if (submit.length) {
                submit.button('disable').button('option', 'label', "Saving, please wait...");
            }
        });

    });
  </script>
</%def>

<%def name="context_menu_items()">
  % if master.viewable and request.has_perm('{}.view'.format(permission_prefix)):
      <li>${h.link_to("View this {}".format(model_title), action_url('view', instance))}</li>
  % endif
  % if master.deletable and instance_deletable and request.has_perm('{}.delete'.format(permission_prefix)):
      <li>${h.link_to("Delete this {}".format(model_title), action_url('delete', instance))}</li>
  % endif
  % if master.creatable and request.has_perm('{}.create'.format(permission_prefix)):
      <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
  % endif
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->
