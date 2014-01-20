$(document).ready(function(){
    $(window).scroll(function() {
	var st = $(window).scrollTop();
        var ot = $("#scroll-anchor").offset().top;
        var s = $(".pagination");
        if(st > ot) {
	    s.css({
                position: "fixed",
                top: "0px",
		'-webkit-box-shadow': '1px 1px 2px 0px rgba(50, 50, 50, 1)',
		'-moz-box-shadow':    '1px 1px 2px 0px rgba(50, 50, 50, 1)',
		'box-shadow':         '1px 1px 2px 0px rgba(50, 50, 50, 1)'
	    });
	    $("#scroll-anchor").css('height', '67px');
        } else {
	    if(st <= ot) {
                s.css({
                    position: "relative",
                    top: "auto",
		    '-webkit-box-shadow': 'none',
		    '-moz-box-shadow': 'none',
		    'box-shadow': 'none'
                });
	    }
	}
    });
});
