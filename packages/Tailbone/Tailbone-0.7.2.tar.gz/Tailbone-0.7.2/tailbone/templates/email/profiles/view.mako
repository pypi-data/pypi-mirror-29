## -*- coding: utf-8 -*-
<%inherit file="/master/view.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  <script type="text/javascript">
    % if not email.get_template('html'):
      $(function() {
          $('#preview-html').button('disable');
          $('#preview-html').attr('title', "There is no HTML template on file for this email.");
      });
    % endif
    % if not email.get_template('txt'):
      $(function() {
          $('#preview-txt').button('disable');
          $('#preview-txt').attr('title', "There is no TXT template on file for this email.");
      });
    % endif
  </script>
</%def>

${parent.body()}

${h.form(url('email.preview'), name='send-email-preview')}
  ${h.csrf_token(request)}
  ${h.link_to("Preview HTML", '{}?key={}&type=html'.format(url('email.preview'), instance['key']), id='preview-html', class_='button', target='_blank')}
  ${h.link_to("Preview TXT", '{}?key={}&type=txt'.format(url('email.preview'), instance['key']), id='preview-txt', class_='button', target='_blank')}
  or
  ${h.text('recipient', value=request.user.email_address or '')}
  ${h.submit('send_{}'.format(instance['key']), value="Send Preview Email")}
${h.end_form()}
