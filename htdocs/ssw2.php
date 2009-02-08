
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<title>Infinite Mosaic - ssw2</title>
<style type="text/css" media="screen">
		<!--
html,body{
	height: 100%;
	margin: 0;
}
div#map{
	height: 100%;
	margin: 0;
}
-->
</style>
		<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAIgkf_4LoiNSc_U8b1dpNDRQgOj4wU9QB2RGC9-bdJnESUNrTNBR1AC9vfcP3RoYOj2QYq2W18mIGrQ" type="text/javascript"></script>
		<script src="http://gmapuploader.com/js/gmapuploader.8.js" type="text/javascript"></script>
	</head>
	<body onunload="GUnload()">
		<div id="map"></div>
		<script type="text/javascript">
//<![CDATA[
var map = new GMap2(document.getElementById("map"));
document.getElementById('map').style.backgroundColor = 'white';
var mapType = new GmapUploaderMapType(map, "http://mt.gmapuploader.com/tiles/6aoN06dmbF", "jpg", 6);
map.setCenter(new GLatLng(0,0), 1, mapType);
map.addControl(new GLargeMapControl());
map.enableContinuousZoom();
//]]>
</script>
	</body>
</html>
