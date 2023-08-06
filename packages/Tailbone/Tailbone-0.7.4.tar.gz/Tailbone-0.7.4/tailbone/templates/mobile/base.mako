## -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>${self.global_title()} &raquo; ${self.title()}</title>
	<meta name="viewport" content="width=device-width, initial-scale=1" />

    ${h.javascript_link('https://code.jquery.com/jquery-1.12.4.min.js')}
    ${h.javascript_link('https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js')}
    ${h.javascript_link(request.static_url('tailbone:static/js/jquery.ui.tailbone.mobile.js'))}
    ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.mobile.js'))}
    ${self.extra_javascript()}

    ## since jquery mobile will "utterly cache" the first page which is loaded
    ## by the client, we must make sure that is always the home page.  so if
    ## user tries to e.g. "refresh" some other page, redirect to home page
    % if request.matched_route.name != 'mobile.home' and request.rattail_config.getbool('tailbone', 'mobile.force_home', default=True):
        <script type="text/javascript">
          location.href = '${request.route_url('mobile.home')}';
        </script>
    % endif

    % if request.rattail_config.getbool('tailbone', 'mobile.flash.autodismiss', default=True):
        <script type="text/javascript">
          $(document).on('pageshow', function() {
              ## TODO: seems like this should be better somehow...
              // remove all flash messages after 2.5 seconds
              window.setTimeout(function() { $('.flash, .error').remove(); }, 2500);
          });
        </script>
    % endif

    ${h.stylesheet_link('https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css')}
    ${h.stylesheet_link(request.static_url('tailbone:static/css/mobile.css'))}
    % if not request.rattail_config.production():
    <style type="text/css">
      .ui-page-theme-a { background-image: url(${request.static_url('tailbone:static/img/testing.png')}); }
    </style>
    % endif
    ${self.extra_styles()}

  </head>
  ${self.mobile_body()}
</html>

<%def name="mobile_body()">
  <body>

    ## note that our toolbars are *external* (in jqm-speak) by default

    ${self.mobile_header()}

    <div data-role="page" data-url="${self.page_url()}"${' data-rel="dialog"' if dialog else ''|n}>

      ${self.mobile_usermenu()}

      ${self.mobile_page_body()}

    </div><!-- page -->

    ${self.mobile_footer()}

  </body>
</%def>

<%def name="app_title()">Rattail Demo</%def>

<%def name="global_title()">${"[STAGE] " if not request.rattail_config.production() else ''}${self.app_title()}</%def>

<%def name="page_url()">${request.current_route_url()}</%def>

<%def name="page_title()">${self.title()}</%def>

<%def name="extra_javascript()"></%def>

<%def name="extra_styles()"></%def>

<%def name="mobile_header()">
  <div data-role="header">
    ${self.mobile_header_link()}
    <h1>${self.global_title()}</h1>
  </div>
</%def>

<%def name="mobile_header_link()">
  <% classes = 'ui-btn-left ui-btn ui-btn-inline ui-mini ui-corner-all ui-btn-icon-left ' %>
  % if request.user:
      ${h.link_to(request.user.get_short_name(), '#usermenu', class_=classes + 'ui-icon-user' + (' root-user' if request.is_root else ''))}
  % elif request.matched_route.name in ('mobile.login', 'mobile.about'):
      ${h.link_to("Home", url('mobile.home'), class_=classes + 'ui-icon-home')}
  % else:
      ${h.link_to("Login", url('mobile.login'), class_=classes + 'ui-icon-user')}
  % endif
</%def>

<%def name="mobile_usermenu()">
  <div id="usermenu" data-role="panel" data-display="overlay">
    <ul data-role="listview">
      <li data-icon="home">${h.link_to("Home", url('mobile.home'))}</li>
      % if request.has_perm('datasync.restart'):
          <li>${h.link_to("DataSync", url('datasync.mobile'))}</li>
      % endif
      % if request.is_root:
          <li class="root-user" data-icon="forbidden">${h.link_to("Stop being root", url('stop_root'), **{'data-ajax': 'false'})}</li>
      % elif request.is_admin:
          <li class="root-user" data-icon="forbidden">${h.link_to("Become root", url('become_root'), **{'data-ajax': 'false'})}</li>
      % endif
      <li data-icon="lock">${h.link_to("Logout", url('mobile.logout'), **{'data-ajax': 'false'})}</li>
      <li data-icon="info">${h.link_to("About {}".format(capture(self.app_title)), url('mobile.about'))}</li>
    </ul>
  </div>
</%def>

<%def name="mobile_page_body()">
  <div role="main" class="ui-content" data-route="${request.matched_route.name}">

    % if request.session.peek_flash('error'):
        % for error in request.session.pop_flash('error'):
            <div class="error">${error}</div>
        % endfor
    % endif

    % if request.session.peek_flash():
        % for msg in request.session.pop_flash():
            <div class="flash">${msg|n}</div>
        % endfor
    % endif

    <h2>${self.page_title()}</h2>

    ${self.body()}

    <div class="replacement-header">
      ${self.mobile_header_link()}
    </div>

  </div>
</%def>

<%def name="mobile_footer()">
  <div data-role="footer">
    <h4>powered by ${h.link_to("Rattail", url('mobile.about'))}</h4>
  </div>
</%def>
