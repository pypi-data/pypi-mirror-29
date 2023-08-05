## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">Delete ${model_title}: ${instance_title}</%def>

<%def name="head_tags()">
  ${parent.head_tags()}
  <script type="text/javascript">
    $(function() {

        $('#confirm-delete').click(function() {
            $(this).button('disable').button('option', 'label', "Deleting, please wait...");
            $(this).parents('form').submit();
        });

    });
  </script>
</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Back to {}".format(model_title_plural), url(route_prefix))}</li>
  % if master.viewable and request.has_perm('{}.view'.format(permission_prefix)):
      <li>${h.link_to("View this {}".format(model_title), action_url('view', instance))}</li>
  % endif
  % if master.editable and request.has_perm('{}.edit'.format(permission_prefix)):
      <li>${h.link_to("Edit this {}".format(model_title), action_url('edit', instance))}</li>
  % endif
  % if master.creatable and request.has_perm('{}.create'.format(permission_prefix)):
      <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
  % endif
</%def>

<%def name="confirmation()">
  <br />
  <p>Are you sure about this?</p>
  <br />

  ${h.form(request.current_route_url())}
  ${h.csrf_token(request)}
    <div class="buttons">
      <a class="button" href="${form.cancel_url}">Whoops, nevermind...</a>
      <button type="button" id="confirm-delete">Yes, please DELETE this data forever!</button>
    </div>
  ${h.end_form()}
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<br />
<p>You are about to delete the following ${model_title} and all associated data:</p>

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->

${self.confirmation()}
