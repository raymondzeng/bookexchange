$(document).ready(function(){
    $('#big-search input').focus();
    $('#nav-search input').focus(function(){
	$('#nav-search input').animate({
	    width: "500px"
	}, {
	    duration: 500
	});
	$('#adv').hide();
    });
    $('#nav-search input').blur(function(){
	$('#nav-search input').animate({
	    width: "300px"
	}, {
	    duration: 500
	});
	$('#adv').show();
    });
    $('.navbar-toggle').click(function(){
	$('#nav-collapse').toggle();
    });
    $('.date').each(function(){
	var date = new Date($(this).html() + ' UTC');
	var s = date.toLocaleDateString();
	$(this).html(s);
    });
});
