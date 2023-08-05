## -*- coding: utf-8 -*-
<%inherit file="/mobile/base.mako" />

<%def name="title()">About ${self.app_title()}</%def>

<h2>${project_title} ${project_version}</h2>

% for name, version in packages.iteritems():
    <h3>${name} ${version}</h3>
% endfor

<p>Please see <a href="https://rattailproject.org/">rattailproject.org</a> for more info.</p>
