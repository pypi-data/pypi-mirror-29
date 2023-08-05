$(document).ready(function() {
  'use strict';
  var reveal_url;
  var uids;
  reveal_url = 'jq_reveal_email';
  if (typeof(portal_url) !== 'undefined') {
	  reveal_url = portal_url + '/' + reveal_url;
  }
  uids = [];
  $('a.hidden-email').each(function() {
    uids.push($(this).attr('rel'));
  });
  if (uids.length) {
    $.pyproxy_call(reveal_url, {'uid': uids});
  }
});
