<?php

require_once 'includes/func.createFlickrApiUrl.php';

function getPhotosByTag($tag){
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

