## -*- coding: utf-8; -*-
<%namespace file="/menu.mako" import="main_menu_items" />
<%namespace file="/grids/nav.mako" import="grid_index_nav" />
<%namespace file="/feedback_dialog.mako" import="feedback_dialog" />
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>${self.global_title()} &raquo; ${capture(self.title)|n}</title>
    ${self.favicon()}
    ${self.header_core()}

    % if not request.rattail_config.production():
        <style type="text/css">
          body { background-image: url(${request.static_url('tailbone:static/img/testing.png')}); }
        </style>
    % endif

    ${self.head_tags()}
  </head>

  <body>
    <div id="body-wrapper">

      <header>
        <nav>
          <ul class="menubar">
            ${main_menu_items()}
          </ul>
        </nav>

        <div class="global">
          <a class="home" href="${url('home')}">
            ${self.header_logo()}
            <span class="title">${self.global_title()}</span>
          </a>
          % if master:
              <span class="global">&raquo;</span>
              % if master.listing:
                  <span class="global">${index_title}</span>
              % else:
                  ${h.link_to(index_title, index_url, class_='global')}
                  % if parent_url is not Undefined:
                      <span class="global">&raquo;</span>
                      ${h.link_to(parent_title, parent_url, class_='global')}
                  % elif instance_url is not Undefined:
                      <span class="global">&raquo;</span>
                      ${h.link_to(instance_title, instance_url, class_='global')}
                  % endif
                  % if master.viewing and grid_index:
                      ${grid_index_nav()}
                  % endif
              % endif
          % endif

          <div class="feedback">
            % if help_url is not Undefined and help_url:
                ${h.link_to("Help", help_url, target='_blank', class_='button')}
            % endif
            <button type="button" id="feedback">Feedback</button>
          </div>

        </div><!-- global -->

        <div class="page">
          ${self.content_title()}
        </div>
      </header>

      <div class="content-wrapper">
        
        <div id="scrollpane">
          <div id="content">
            <div class="inner-content">

              % if request.session.peek_flash('error'):
                  <div class="error-messages">
                    % for error in request.session.pop_flash('error'):
                        <div class="ui-state-error ui-corner-all">
                          <span style="float: left; margin-right: .3em;" class="ui-icon ui-icon-alert"></span>
                          ${error}
                        </div>
                    % endfor
                  </div>
              % endif

              % if request.session.peek_flash():
                  <div class="flash-messages">
                    % for msg in request.session.pop_flash():
                        <div class="ui-state-highlight ui-corner-all">
                          <span style="float: left; margin-right: .3em;" class="ui-icon ui-icon-info"></span>
                          ${msg|n}
                        </div>
                    % endfor
                  </div>
              % endif

              ${self.body()}

            </div><!-- inner-content -->
          </div><!-- content -->
        </div><!-- scrollpane -->

      </div><!-- content-wrapper -->

      <div id="footer">
        ${self.footer()}
      </div>

    </div><!-- body-wrapper -->

    ${feedback_dialog()}
  </body>
</html>

<%def name="app_title()">Rattail</%def>

<%def name="global_title()">${"[STAGE] " if not request.rattail_config.production() else ''}${self.app_title()}</%def>

<%def name="title()"></%def>

<%def name="content_title()">
  <h1>${self.title()}</h1>
</%def>

<%def name="favicon()"></%def>

<%def name="header_core()">
  ${self.core_javascript()}
  ${self.extra_javascript()}
  ${self.core_styles()}
  ${self.extra_styles()}

  ## TODO: should this be elsewhere / more customizable?
  % if dform is not Undefined:
      <% resources = dform.get_widget_resources() %>
      % for path in resources['js']:
          ${h.javascript_link(request.static_url(path))}
      % endfor
      % for path in resources['css']:
          ${h.stylesheet_link(request.static_url(path))}
      % endfor
  % endif
</%def>

<%def name="core_javascript()">
  ${h.javascript_link('https://code.jquery.com/jquery-1.12.4.min.js')}
  ${h.javascript_link('https://code.jquery.com/ui/{}/jquery-ui.min.js'.format(request.rattail_config.get('tailbone', 'jquery_ui.version', default='1.11.4')))}
  ${h.javascript_link(request.static_url('tailbone:static/js/lib/jquery.ui.menubar.js'))}
  ${h.javascript_link(request.static_url('tailbone:static/js/lib/jquery.loadmask.min.js'))}
  ${h.javascript_link(request.static_url('tailbone:static/js/lib/jquery.ui.timepicker.js'))}
  <script type="text/javascript">
    var session_timeout = ${request.get_session_timeout() or 'null'};
    var logout_url = '${request.route_url('logout')}';
    var noop_url = '${request.route_url('noop')}';
  </script>
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.js') + '?ver={}'.format(tailbone.__version__))}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.feedback.js') + '?ver={}'.format(tailbone.__version__))}
  ${h.javascript_link(request.static_url('tailbone:static/js/jquery.ui.tailbone.js') + '?ver={}'.format(tailbone.__version__))}
</%def>

<%def name="extra_javascript()"></%def>

<%def name="core_styles()">
  ${h.stylesheet_link(request.static_url('tailbone:static/css/normalize.css'))}
  ${self.jquery_theme()}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/jquery.ui.menubar.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/jquery.loadmask.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/jquery.ui.timepicker.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/jquery.ui.tailbone.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/base.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/layout.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/grids.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/filters.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/forms.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/diffs.css') + '?ver={}'.format(tailbone.__version__))}
</%def>

<%def name="jquery_theme()">
  ${h.stylesheet_link('https://code.jquery.com/ui/1.11.4/themes/dark-hive/jquery-ui.css')}
</%def>

<%def name="extra_styles()"></%def>

<%def name="head_tags()"></%def>

<%def name="header_logo()"></%def>

<%def name="footer()">
  powered by ${h.link_to("Rattail", url('about'))}
</%def>

<%def name="wtfield(form, name, **kwargs)">
  <div class="field-wrapper${' error' if form[name].errors else ''}">
    <label for="${name}">${form[name].label}</label>
    <div class="field">
      ${form[name](**kwargs)}
    </div>
  </div>
</%def>
