/**
 * Created by haohao on 17-3-4.
 */

$(document).ready(function(){

    $(".dropdown").hover(

        function() {

            $('.dropdown-menu', this).not('.in .dropdown-menu').stop( true, true ).slideDown("fast");

            $(this).toggleClass('open');

        },

        function() {

            $('.dropdown-menu', this).not('.in .dropdown-menu').stop( true, true ).slideUp("fast");

            $(this).toggleClass('open');

        }

    );

});


var collect_article = document.getElementsByClassName("collect_article")

function collectArticle(){

}