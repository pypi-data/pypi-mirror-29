## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">Login</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  ${h.javascript_link(request.static_url('tailbone:static/js/login.js'))}
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/login.css'))}
</%def>

<%def name="logo()">
  ${h.image(image_url, "{} logo".format(capture(self.app_title)), id='logo', width=500)}
</%def>

<%def name="login_form()">
  <div class="form">
    ${form.render_deform(form_kwargs={'data-ajax': 'false'})|n}
  </div>
</%def>

${self.logo()}

${self.login_form()}

% if request.rattail_config.demo():
    <p class="tips">
      Login with <strong>chuck / admin</strong> for full demo access
    </p>
% endif
