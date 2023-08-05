## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">Home</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">
    .logo {
        text-align: center;
    }
    .logo img {
        margin: 3em auto;
    }
  </style>
</%def>

<div class="logo">
  ${h.image(image_url, "{} logo".format(capture(self.app_title)), id='logo', width=500)}
  <h1>Welcome to ${self.app_title()}</h1>
</div>
