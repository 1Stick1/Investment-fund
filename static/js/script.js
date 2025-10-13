function calculate() {
  const currency = document.getElementById("currency").value;
  const amount = parseFloat(document.getElementById("amount").value);
  const termInput = document.getElementById("term").value;
  const rate = parseFloat(document.getElementById("rate").value);

  const term = parseFloat(termInput);

  const profitSpan=document.getElementById("profit");
  const totalSpan=document.getElementById("total");

  if (isNaN(amount) || isNaN(term) || isNaN(rate)) {
    profitSpan.textContent ="Błąd danych";
    totalSpan.textContent ="-";
    return;
  }
  const monthlyRate = rate / 12 / 100;
  const finalAmount = amount * Math.pow(1 + monthlyRate, term);
  const profit = finalAmount - amount;

  profitSpan.textContent =`${profit.toFixed(2)}${currency}`;
totalSpan.textContent = `${finalAmount.toFixed(2)} ${currency}`;

}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("button").addEventListener("click", calculate);
});


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
    msg.textContent = "❌ Hasło musi mieć co najmniej 8 znaków, zawierać małą i wielką literę oraz symbol (np. !@#).";
    msg.style.color = "red";
    return;
  }

  if (pw !== pw2) {
    msg.textContent = "❌ Hasła nie pasują.";
    msg.style.color = "red";
    return;
  }
  msg.textContent = "✅ Hasła pasują!";
  msg.style.color = "green";
  form.submit();
});
