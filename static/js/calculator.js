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