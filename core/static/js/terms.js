function showTermsAndConditionsAlert(){
  termsAgreed = localStorage.getItem("terms-agreed");
  termsDiv = document.getElementById("terms-alert");
  if(JSON.parse(termsAgreed)===true && termsAgreed !== null) {
    termsDiv.style.display = "none";
  } else {
    termsDiv.style.display = "block";
  }
}

function agreeTerms() {
  localStorage.setItem("terms-agreed", true);
}