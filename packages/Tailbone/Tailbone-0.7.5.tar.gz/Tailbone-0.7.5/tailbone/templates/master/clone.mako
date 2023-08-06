## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">Clone ${model_title}: ${instance_title}</%def>

<br />
<p>You are about to clone the following ${model_title} as a new record:</p>

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->

<br />
<p>Are you sure about this?</p>
<br />

${h.form(request.current_route_url(), class_='autodisable')}
${h.csrf_token(request)}
${h.hidden('clone', value='clone')}
  <div class="buttons">
    ${h.link_to("Whoops, nevermind...", form.cancel_url, class_='button autodisable')}
    ${h.submit('submit', "Yes, please clone away")}
  </div>
${h.end_form()}
