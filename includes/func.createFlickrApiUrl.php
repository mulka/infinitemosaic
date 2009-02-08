<?php

require_once 'includes/config.php';

function createFlickrApiUrl($method, $params = array()){
	global $flickrApiKey;
	$params['api_key'] = $flickrApiKey;
	$params['method'] = $method;
	return 'http://api.flickr.com/services/rest/?'.http_build_query($params);
}

