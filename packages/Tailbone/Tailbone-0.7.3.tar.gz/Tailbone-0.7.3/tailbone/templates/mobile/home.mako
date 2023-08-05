## -*- coding: utf-8 -*-
<%inherit file="/mobile/base.mako" />

<%def name="title()">Home</%def>

<%def name="page_title()"></%def>

<div style="text-align: center;">
  ${h.image(image_url, "{} logo".format(capture(self.app_title)), id='logo', width=300)}
  <h3>Welcome to ${self.app_title()}</h3>
</div>
