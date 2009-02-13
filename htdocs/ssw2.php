<?php

if(strstr($_SERVER['HTTP_USER_AGENT'], 'iPhone')){
	header('Location: deepzoom://dz.gmapuploader.com/7kBfnUeTsS.xml');
	exit();
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<title>Infinite Mosaic for Seattle Startup Weekend 2 (ssw2)</title>
<style>
img {
	border: none;
}
</style>
</head>
<body>
<center>
<div>
<a href="http://blog.infinitemosaic.com"><img src="/images/logo.png" width="295" height="83"></a><br>
<a href="http://blog.infinitemosaic.com">More Info</a> | <a href="http://blog.infinitemosaic.com/?page_id=20">Sign Up</a>
</div>
</center>
<script type="text/javascript" src="http://seadragon.com/ajax/embed.js"></script><script type="text/javascript">Seadragon.embed("100%", "512px", "http://dz.gmapuploader.com/7kBfnUeTsS.xml", 8192, 8192, 256, 0, "jpg");</script>
</body>
</html>

