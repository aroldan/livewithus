(function($) {
  var cache = [];
  // Arguments are image paths relative to the current page.
  $.preLoadImages = function() {
    var args_len = arguments.length;
    for (var i = args_len; i--;) {
      var cacheImage = document.createElement('img');
      cacheImage.src = arguments[i];
      cache.push(cacheImage);
    }
  }
})(jQuery)

$(document).ready(function() {
	jQuery.preLoadImages("/site_media/img/frontpage/share.png", "/site_media/img/frontpage/organize.png", "/site_media/img/frontpage/decide.png");
	$("#features-select li").mouseenter(function(event) {
		var this_text = $(this).text().toLowerCase()
		$("#lwu-stuff-left img").attr("src", "/site_media/img/frontpage/" + this_text + ".png");
	});
	$("#lwu-stuff-left img").mouseenter(function(event) {
		$("#lwu-stuff-left img").attr("src", "/site_media/img/frontpage/home.png");
	});
});