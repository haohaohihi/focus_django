/**
 * Created by haohao on 17-3-4.
 */

$(document).ready(function () {

    $(".dropdown").hover(
        function () {
            $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true, true).slideDown("fast");
            $(this).toggleClass('open');
        },
        function () {
            $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true, true).slideUp("fast");
            $(this).toggleClass('open');
        }
    );
});


function collectArticle(article_id) {
    if (sessionStorage.getItem("status") === null)
        alert("请登陆后进行收藏");
    else {
        var l_star = document.getElementById("l" + article_id);
        var s_star = document.getElementById("s" + article_id);
        console.log(l_star);
        console.log(s_star);
        if (l_star.getAttribute("fill") === "grey") {
            $.post('/add_or_cancel_collection', {
                article_id: article_id,
                valid: 1
            }, function (result) {
                var result_json = JSON.parse(result);
                if(result_json.status === 0){
                    alert("收藏成功");
                    l_star.setAttribute("fill", "yellow");
                    s_star.setAttribute("fill", "yellow");
                }
                else
                    alert(result_json.message);

            })
                .fail(function () {
                    alert("收藏失败")
                });
        }
        else {
            $.post('/add_or_cancel_collection', {
                article_id: article_id,
                valid: 0
            }, function (result) {
                var result_json = JSON.parse(result);
                if(result_json.status === 0){
                    alert("取消收藏成功");
                    l_star.setAttribute("fill", "grey");
                    s_star.setAttribute("fill", "grey");
                }
                else
                    alert(result_json.message);
            })
                .fail(function () {
                    alert("取消收藏失败")
                });
        }
    }
}

function doLogout() {
    sessionStorage.removeItem('status');
}