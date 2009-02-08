<?php

require_once 'includes/config.php';

$i = 1;
exec("wget -O $i.xml 'http://api.flickr.com/services/rest/?api_key=$flickrApiKey&method=flickr.photos.search&per_page=50&page=$i'");
