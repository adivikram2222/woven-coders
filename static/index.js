$(document).ready(function(){

  $('#menu').click(function(){
    $(this).toggleClass('fa-times');
    $('header').toggleClass('toggle');
  });

  $(window).on('scroll load',function(){

    $('#menu').removeClass('fa-times');
    $('header').removeClass('toggle');

    if($(window).scrollTop() > 0){
      $('.top').show();
    }else{
      $('.top').hide();
    }

  });

  // smooth scrolling 

  $('a[href*="#"]').on('click',function(e){

    e.preventDefault();

    $('html, body').animate({

      scrollTop : $($(this).attr('href')).offset().top,

    },
      500, 
      'linear'
    );

  });

});












const input = document.querySelector("input"),
emailIcon = document.querySelector(".email-icon")

input.addEventListener("keyup", () => {
let pattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

if (input.value === "") {
    emailIcon.classList.replace("uil-check-circle", "uil-envelope");
    return emailIcon.style.color = "#b4b4b4";
}
if (input.value.match(pattern)) {
    emailIcon.classList.replace("uil-envelope", "uil-check-circle");
    return emailIcon.style.color = "#4bb543"
}
emailIcon.classList.replace("uil-check-circle", "uil-envelope");
emailIcon.style.color = "#de0611"
})

function checkPassword() {
var password = document.getElementById("password").value;
var cPassword = document.getElementById("c-password").value;
var message = document.getElementById("message");
if (password == cPassword) {
    message.textContent = "Passwords Match";
    message.style.backgroundColor = "green";
} else {
    message.textContent = "Passwords don't Match";
    message.style.backgroundColor = "red";
}
}