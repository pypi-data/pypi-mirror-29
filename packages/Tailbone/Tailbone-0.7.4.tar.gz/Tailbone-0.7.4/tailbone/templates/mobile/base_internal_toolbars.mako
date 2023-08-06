## -*- coding: utf-8 -*-
<%inherit file="tailbone:templates/mobile/base.mako" />

<%def name="mobile_body()">
  <body>

    <div data-role="page" data-url="${self.page_url()}"${' data-rel="dialog"' if dialog else ''|n}>

      ${self.mobile_usermenu()}

      ${self.mobile_header()}

      ${self.mobile_page_body()}

      ${self.mobile_footer()}

    </div><!-- page -->

  </body>
</%def>
