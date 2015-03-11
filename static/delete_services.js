/**
 * Created by roeder on 3/9/15.
 */
var current_position1 = 0;
var main = function(){

   $('.icon-menu').click( function(){
       $('.menu').animate({
           right: '0px'
           }, 200);
    $('body').animate({
        right: '285px'
    }, 200);
   });

   $('.icon-close').click( function(){
        $('.menu').animate({
            right: '-285px'
            }, 200);
        $('body').animate({
            right: '0px'
        }, 200);
   });

    $('.icon-menu').dblclick( function(){
           if( current_position1 === 285 ) {
               $('.menu').animate({
                   right: '-285px'
               }, 200);
               $('body').animate({
                   right: '0px'
               }, 200);
               current_position1 = 0;
           }
   });
};

$(document).ready(main);