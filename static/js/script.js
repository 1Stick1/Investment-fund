
const form = document.getElementById('signup');
const password = document.getElementById('password');
const password_again = document.getElementById('password_again');
const msg = document.getElementById('msg');

const pwRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9]).{8,}$/;

form.addEventListener('submit', function (e) {
  e.preventDefault();

  const pw = password.value;
  const pw2 = password_again.value;

  if (!pwRegex.test(pw)) {
    msg.textContent = " Hasło musi mieć co najmniej 8 znaków, zawierać małą i wielką literę oraz symbol (np. !@#).";
    msg.style.color = "red";
    return;
  }

  if (pw !== pw2) {
    msg.textContent = " Hasła nie pasują.";
    msg.style.color = "red";
    return;
  }
  msg.textContent = " Hasła pasują!";
  msg.style.color = "green";
  form.submit();
});
