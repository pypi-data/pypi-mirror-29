## -*- coding: utf-8; -*-
<%namespace file="tailbone:templates/base.mako" import="core_javascript" />
<%namespace file="/base.mako" import="jquery_theme" />
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html style="direction: ltr;" xmlns="http://www.w3.org/1999/xhtml" lang="en-us">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>${initial_msg or "Working"}...</title>
    ${core_javascript()}
    ${h.stylesheet_link(request.static_url('tailbone:static/css/normalize.css'))}
    ${jquery_theme()}
    ${h.stylesheet_link(request.static_url('tailbone:static/css/base.css'))}
    ${h.stylesheet_link(request.static_url('tailbone:static/css/layout.css'))}
    ${h.stylesheet_link(request.static_url('tailbone:static/css/progress.css'))}
    ${self.update_progress_func()}
    ${self.extra_styles()}
    <script type="text/javascript">

      var updater = null;

      updater = setInterval(function() {update_progress()}, 1000);

      $(function() {

          $('#cancel button').click(function() {
              if (confirm("Do you really wish to cancel this operation?")) {
                  clearInterval(updater);
                  $(this).button('disable').button('option', 'label', "Canceling, please wait...");
                  $.ajax({
                      url: '${url('progress', key=progress.key)}?sessiontype=${progress.session.type}',
                      data: {
                          'cancel_msg': '${cancel_msg}',
                      },
                      success: function(data) {
                          location.href = '${cancel_url}';
                      },
                  });
              }
          });

      });

      </script>
  </head>
  <body>
    <div id="body-wrapper">

      <div id="wrapper">

        <p><span id="message">${initial_msg or "Working"} (please wait)</span> ... <span id="total"></span></p>

        <table id="progress-wrapper">
          <tr>
            <td>
              <table id="progress">
                <tr>
                  <td id="complete"></td>
                  <td id="remaining"></td>
                </tr>
              </table><!-- #progress -->
            </td>
            <td id="percentage"></td>
            <td id="cancel">
              <button type="button" style="display: none;">Cancel</button>
            </td>
          </tr>
        </table><!-- #progress-wrapper -->

      </div><!-- #wrapper -->

      ${self.after_progress()}

    </div><!-- #body-wrapper -->
  </body>
</html>

<%def name="update_progress_func()">
  <script type="text/javascript">

      function update_progress() {
          $.ajax({
              url: '${url('progress', key=progress.key)}?sessiontype=${progress.session.type}',
              success: function(data) {
                  if (data.error) {
                      location.href = '${cancel_url}';
                  } else if (data.complete || data.maximum) {
                      $('#message').html(data.message);
                      $('#total').html('('+data.maximum_display+' total)');
                      $('#cancel button').show();
                      if (data.complete) {
                          clearInterval(updater);
                          $('#cancel button').hide();
                          $('#total').html('done!');
                          $('#complete').css('width', '100%');
                          $('#remaining').hide();
                          $('#percentage').html('100 %');
                          location.href = data.success_url;
                      } else {
                          var width = parseInt(data.value) / parseInt(data.maximum);
                          width = Math.round(100 * width);
                          if (width) {
                              $('#complete').css('width', width+'%');
                              $('#percentage').html(width+' %');
                          } else {
                              $('#complete').css('width', '0.01%');
                              $('#percentage').html('0 %');
                          }
                          $('#remaining').css('width', 'auto');
                      }
                  }
              },
          });
      }
  </script>
</%def>

<%def name="extra_styles()"></%def>

<%def name="after_progress()"></%def>
