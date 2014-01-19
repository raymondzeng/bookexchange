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
    $('.date').each(function(){
	var date = new Date($(this).html() + ' UTC');
	var s = date.toLocaleDateString();
	$(this).html(s);
    });
    $('.td-button').click(function(){
	if(confirm('Are you sure you want to delete this post? Can not be undone')){
	    $(document.body).append('<form id="deletepost" action="/delete" method="POST"><input type="hidden" name="id" value="' + $(this).attr('id') + '"></form>')
	    $('#deletepost').submit();
	}
    });

    $('.sub-x').click(function(){
	$(document.body).append('<form id="unsub" action="/unsubscribe" method="POST"><input type="hidden" name="isbn" value="' + $(this).attr('isbn') + '"></form>')
	$('#unsub').submit();
    });

    $('#isbn').on('input',function(){
	if($(this).val().trim() == '')
	    return;
	getPreview();
    });
    $('.fblink').click(function(){
	window.open($(this).attr('link'));
    });
    
    if($('#isbn').val() != '')
	getPreview();
    $('#save').click(function(){
	$('#settings').submit();
    });
});

function getPreview(){
    $('#bookimg').css('display','block');
    $('#imgp').css('display','none');
    $('#prev-info').html('If this book is on sold on Amazon, there should be preview information. Make sure the ISBN-13 # is correct.');
    $('#bookimg').attr('src','/static/spinner.gif');
    $.get('/info/' + $('#isbn').val()).done(function(data){
	if(data.title == null){
	    $('#bookimg').css('display','none');
	    $('#imgp').css('display','block');
	    $('#prev-info').html('If this book is on sold on Amazon, there should be preview information. Make sure the ISBN-13 # is correct.');
	    $('#prev-info').css('display','block');
	}
	else{
	    $('#bookimg').attr('src',data.image);
	    $('#imgp').css('display','none');
	    var title, author;
	    if(data.title == null)
		title = 'No Title Available';
	    else
		title = data.title;
	    author = ''
	    if(data.author != null){
		author = data.author[0];
		for(var i = 1; i < data.author.length; i++)
		    author = author.concat(' | '+data.author[i]);
	    }
	    console.log(author);
	    $('#prev-info').html('<label>'+title+'</label><p>'+author+'</p>');
	}
    });
}
