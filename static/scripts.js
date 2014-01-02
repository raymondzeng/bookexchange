$(document).ready(function(){
    $('#searchbar').focus(function(){
	$('#searchbar').animate({
	    width: "400px"
	}, {
	    duration: 500
	});
	$('#as-button').toggle();
    });
    $('#searchbar').blur(function(){
	$('#searchbar').animate({
	    width: "181px"
	}, {
	    duration: 500
	});
	$('#as-button').toggle();
    });
    $("#as-button").click(function(){
	$("#advancedsearch").slideToggle();
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
