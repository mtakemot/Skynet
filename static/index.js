/*var main = function() {
    $('.dropdown-toggle').click(function() {
        $('.dropdown-menu').toggle();
    });

    $('.dropdown1-toggle').click(function() {
        $('.dropdown1-menu').toggle();
    });
};

   $(document).ready(main); */

var main = function(){

    $('.icon-menu0').click( function(){
       $('.menu0').animate({
           right: '0px'
           }, 200);
    $('body').animate({
        right: '285px'
    }, 200);
   });

   $('.icon-close0').click( function(){
        $('.menu0').animate({
            right: '-285px'
            }, 200);
        $('body').animate({
            right: '0px'
        }, 200);
   });

   $('.icon-menu1').click( function(){
       $('.menu1').animate({
           right: '0px'
           }, 200);
    $('body').animate({
        right: '285px'
    }, 200);
   });

   $('.icon-close1').click( function(){
        $('.menu1').animate({
            right: '-285px'
            }, 200);
        $('body').animate({
            right: '0px'
        }, 200);
   });
};

$(document).ready(main);