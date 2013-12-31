$(document).ready(function(){
    $("#search-a").click(function(){
	if($("#searchbar").css('display') == 'none'){
	    $("#searchbar").slideToggle();
	    $("#searchbar input").focus();
	}
	else
	    $("#searchbar").slideToggle();
    });
    $("#as-button").click(function(){
	$("#advancedsearch").slideToggle();
	$("#searchbar input").focusout();
    });
    $("#as-cancel").click(function(){
	$("#advancedsearch").slideToggle();
    });
});
