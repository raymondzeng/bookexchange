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
    $('#register-submit').click(function(){
	validate_reg();
    });
});

function validate_reg(){
    $.getJSON('/validate_email',{
        e: $('#register-email').val()
    }, function(data){
	// email taken
	if(data.result)
	    // do smthng when email taken
	    console.log("email taken");
	else if($('#register-password').val() != $('#register-reenter').val())
	    //do smthng when passwords dont match
	    console.log("passwords don't match")
	else
	    submit_reg();
    });
}

function submit_reg(){
    $.getJSON('/register',{
        e: $('#register-email').val(),
	p: $('#register-password').val()
    });
}
