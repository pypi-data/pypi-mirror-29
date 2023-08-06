## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/create.mako" />

<%def name="title()">${h.link_to("Inventory", url('mobile.batch.inventory'))} &raquo; New Batch</%def>

${parent.body()}
