
$(document).ready(function() {
	'use strict';

	/*--------------------------------------------
	togglePassword
	--------------------------------------------*/

  function togglePassword(){
      let input = document.getElementById("inputPass");
      var eye = document.getElementById("eye");
      var eyeSlash = document.getElementById("eye-slash");

      if(input.type === "password"){
          input.type = "text"
          eye.style.display = "none";
          eyeSlash.style.display = "inline";
      } else {
          input.type = "password"
          eye.style.display = "inline";
          eyeSlash.style.display = "none";
      }
  }

  $('.pass-toggler-btn').on('click', 'i', function() {
  	togglePassword();
  })


})