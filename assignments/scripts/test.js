/* 
$('#right-arrow').click(function() {
    var currentSlide = $('.slide.active');
    var nextSlide = currentSlide.next();
    
    currentSlide.fadeOut(300).removeClass('active');
    nextSlide.fadeIn(300).addClass('active');
    
    if(nextSlide.length == 0) {
        $('.slide').first().fadeIn(300).addClass('active');
    }
})


$('#left-arrow').click(function() {
     var currentSlide = $('.slide.active');
    var prevSlide = currentSlide.prev();
    
    currentSlide.fadeOut(300).removeClass('active');
    prevSlide.fadeIn(300).addClass('active');
    
    if(prevSlide.length == 0) {
        $('.slide').last().fadeIn(300).addClass('active');
    }
})
*/

$(document).ready(function(){
    $('.next').on('click', function(){
        var currentImg = $('.active');
        var nextImg = currentImg.next();
        
        if(nextImg.length){
            currentImg.removeClass('active').css('z-index', -10);
            nextImg.addClass('active').css('z-index', 10);
        }
    });
    
     $('.prev').on('click', function(){
        var currentImg = $('.active');
        var prevImg = currentImg.next();
        
        if(prevImg.length){
            currentImg.removeClass('active').css('z-index', -10);
            prevImg.addClass('active').css('z-index', 10);
        }
    });
});