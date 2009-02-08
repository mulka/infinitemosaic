<?php

require_once 'includes/config.php';

function createFlickrApiUrl($method, $params = array()){
	global $flickrApiKey;
	$params['api_key'] = $flickrApiKey;
	$params['method'] = $method;
	return 'http://api.flickr.com/services/rest/?'.http_build_query($params);
}

function getPhotosByTag($tag){
	global $api;

	$rv = array();
	
	$page = 1;
	do{
		$xml = simplexml_load_file(createFlickrApiUrl('flickr.photos.search', array('tags' => $tag, 'per_page' => 50, page => $page)));

		foreach($xml->photos->photo as $photo){
			$a = $photo->attributes();
			$photoUrl = "http://farm{$a->farm}.static.flickr.com/{$a->server}/{$a->id}_{$a->secret}_s.jpg";
			array_push($rv, array('id' => (int)$a->id, 'url' => $photoUrl));
		}
		$page++;
	}while($page <= $xml->photos->attributes()->pages);
	return $rv;
}

