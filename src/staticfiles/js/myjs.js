$(document).ready(function(){
    $('.toast').toast('show');
    $(".comment-reply-btn").click(function(event){
        event.preventDefault();
        $(this).parent().next(".comment-reply").fadeToggle();
    })
})