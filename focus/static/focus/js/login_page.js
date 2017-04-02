/**
 * Created by haohao on 17-3-27.
 */
$(function () {

    $('#login-form-link').click(function (e) {
        $("#login-form").delay(100).fadeIn(100);
        $("#register-form").fadeOut(100);
        $('#register-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });
    $('#register-form-link').click(function (e) {
        $("#register-form").delay(100).fadeIn(100);
        $("#login-form").fadeOut(100);
        $('#login-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });

});


var login_username = document.getElementById("login-username");
var login_password = document.getElementById("login-password");

function doLogIn(){
    $.post('/login',{
        username: login_username.value,
        password: login_password.value
    }, function(result){
        var result_json = JSON.parse(result);
        console.log(result_json.status);
        if (result_json.status === 0){
            alert(result_json.message);
            window.location.href="/";
        }
        else{
            alert(result_json.message);
            window.location.href="/login_page";
        }
    });
}


var register_username = document.getElementById("register-username");
var register_password = document.getElementById("register-password");
var email = document.getElementById("email");
var register_confirm_password = document.getElementById("register-confirm-password");

function doRegister(){
    if (register_password.value != register_confirm_password.value) {
        alert("密码不一致!");
        return false;
    }
    $.post('/register', {
        username: register_username.value,
        email: email.value,
        password: register_password.value,
        confirm_password: register_confirm_password.value
    }, function (result) {
        var result_json = JSON.parse(result);
        console.log(result_json.status);
        if (result_json.status == 0) {
            alert('注册成功,请登陆！');
            window.location.href = "/login_page";
        }
        else {
            alert(result_json.message);
        }
    });
}