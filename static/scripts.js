$(document).ready(function(){
    $("#search-a").click(function(){
	$("#searchbar").slideToggle();
	$("#searchbar input").focus();
    });
    $("#as-button").click(function(){
	$("#advancedsearch").slideToggle();
    });
    $("#as-cancel").click(function(){
	$("#advancedsearch").slideToggle();
    });
});
