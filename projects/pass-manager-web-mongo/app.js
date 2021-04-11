// SELECTORS 
const navBtn = document.querySelector('.nav-btn');
const navbar = document.querySelector('.navbar');
const closeNavBtn = document.querySelector('.close-btn');

//VARIABLES 


//MOBILE NAV BUTTON
navBtn.addEventListener('click', function() {
  navbar.classList.remove('hide');
});

closeNavBtn.addEventListener('click', function() {
  navbar.classList.add('hide');
})