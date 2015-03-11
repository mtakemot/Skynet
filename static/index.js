/*var main = function() {
    $('.dropdown-toggle').click(function() {
        $('.dropdown-menu').toggle();
    });

    $('.dropdown1-toggle').click(function() {
        $('.dropdown1-menu').toggle();
    });
};

   $(document).ready(main); */
var current_position1 = 0;
var current_position2 = 0;
var main = function(){

    $('.icon-menu0').click( function(){
       $('.menu0').animate({
           right: '0px'
           }, 200);
    $('body').animate({
        right: '285px'
    }, 200);
        current_position1 = 285;
   });

   $('.icon-close0').click( function(){
        $('.menu0').animate({
            right: '-285px'
            }, 200);
        $('body').animate({
            right: '0px'
        }, 200);
       current_position1 = 0;
   });

       $('.icon-menu0').dblclick( function(){
           if( current_position1 === 285 ) {
               $('.menu0').animate({
                   right: '-285px'
               }, 200);
               $('body').animate({
                   right: '0px'
               }, 200);
               current_position1 = 0;
           }
   });


   $('.icon-menu1').click( function(){
       $('.menu1').animate({
           right: '0px'
           }, 200);
    $('body').animate({
        right: '285px'
    }, 200);
       current_position2 = 285;
   });

   $('.icon-close1').click( function(){
        $('.menu1').animate({
            right: '-285px'
            }, 200);
        $('body').animate({
            right: '0px'
        }, 200);
        current_position2 = 0;
   });


       $('.icon-menu1').dblclick( function(){
           if( current_position2 === 285 ) {
               $('.menu1').animate({
                   right: '-285px'
               }, 200);
               $('body').animate({
                   right: '0px'
               }, 200);
               current_position2 = 0;
           }
   });

};

$(document).ready(main);