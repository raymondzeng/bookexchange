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
	if(confirm("Are you sure you want to delete this post? This cannot be undone")){
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
    
    if($('#isbn').val() != '')
	getPreview();
    
    $('#save').click(function(){
	$('#settings').submit();
    });
    
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-47415608-1']);
    _gaq.push(['_trackPageview']);
    
    (function() {
	var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
	ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
	var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    })();
    
    var num = 1;
    $('.restable').each(function(){
	$(this).attr('id',"res"+num);
	$(this).hide();
	num++;
    });    

    var tables = $('tables').length;
    $('#res1').show();
    $('#resa1').addClass('active');
    $(".resa").click(function (e) {
        e.preventDefault();
	n = $(this).attr('num');
        $("#res" + n).show().siblings('table').hide();
	$('.pagination li').each(function() {
	    $(this).removeClass('active');
	});
	$('#resa' + n).addClass('active');
    });
    
    $('#resprev').click(function(){
	currentPage = $('[class=active]').attr('id')[4];
	if (currentPage == 1)
	    return;
	else{
	    $('#resa' + (currentPage - 1) + " a").click();
	}
    });

    $('#resnext').click(function(){
	currentPage = $('[class=active]').attr('id')[4];
	if (currentPage == tables)
	    return;
	else{
	    currentPage++;
	    $('#resa'+(currentPage)+' a').click();
	}
    });    

    $('.edit-button').click(function(){
	$('#editid').attr('value', $(this).attr('pid'));
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
	    var title, author, courses;
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
	    courses = ''
	    if(data.courses != null){
		courses = data.courses[0];
		for(var i = 1; i < data.courses.length; i++)
		    courses = courses.concat(' | '+data.courses[i]);
	    }
	$('#prev-info').html('<label>'+title+'</label><p>'+author+'</p>'+'<p>Courses: '+courses+'</p>');
    }
    });
}


