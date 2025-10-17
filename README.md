# Fundusz Inwestycyjny RamBad - Aplikacja Webowa

## Opis projektu
Projekt przedstawia stronę internetową dla **funduszu inwestycyjnego otwartego**, który zbiera środki od inwestorów i umożliwia ich wypłatę w dowolnym czasie. Zebrane środki są inwestowane w proporcji: **60% w akcje z USA(S&P 500)** i **40% w obligacje państw UE należących do strefy Euro(STOXX 50 (UE))**.  

Aplikacja umożliwia użytkownikom:
- przeglądanie stanu swojego portfela w PLN,
- symulację wyników inwestycji w PLN,
- deklarowanie wpłat i wypłat.


## Technologie
- **Backend:** Python, Flask  
- **Baza danych:** SQLite3  
- **Frontend:** HTML, CSS, JavaScript  
- **Metodologia CSS:** BEM (Blok-Element-Modifier)  
- **Inne:** [tutaj można dodać dodatkowe technologie lub biblioteki, jeśli pamiętasz]


## Funkcjonalności
- Rejestracja i logowanie użytkowników  
- Dashboard inwestycyjny z podglądem środków  
- Symulacja wyników inwestycyjnych  
- Deklarowanie wpłat i wypłat środków  
- Walidacja danych wejściowych


## Testy bezpieczeństwa

Projekt był testowany przy użyciu **OWASP ZAP**. Wykryto między innymi następujące problemy:

- **Absence of Anti-CSRF Tokens (6)**  
  Formularze i endpointy nie zawierają tokenów anty-CSRF, co zwiększa ryzyko nieautoryzowanych akcji użytkownika.

- **Content Security Policy (CSP) Header Not Set (12)**  
  Brak nagłówka CSP, co zwiększa ryzyko XSS i ładowania niebezpiecznych zasobów.

- **Cross-Domain Misconfiguration**  
  Niewłaściwa konfiguracja CORS może umożliwiać dostęp z nieautoryzowanych domen.

- **Missing Anti-clickjacking Header (7)**  
  Brak nagłówka X-Frame-Options pozwala na osadzanie strony w iframe i ataki typu clickjacking.

- **Application Error Disclosure (2)**  
  Aplikacja ujawnia szczegółowe informacje o błędach i stacktrace, co może pomóc atakującemu.

- **Cookie Without Secure Flag (2)**  
  Ciasteczka sesyjne bez flagi Secure mogą być przechwycone przy połączeniu HTTP.

- **Cookie without SameSite Attribute (2)**  
  Brak atrybutu SameSite zwiększa ryzyko CSRF i niepożądanych przesyłek ciasteczek.

- **Cross-Domain JavaScript Source File Inclusion (2)**  
  Wczytywanie skryptów z zewnętrznych domen zwiększa ryzyko wstrzyknięcia złośliwego kodu.

- **Information Disclosure - Debug Error Messages (2)**  
  Debug/error messages ujawniają informacje o technologii i strukturze aplikacji.

- **Strict-Transport-Security Header Not Set (22)**  
  Brak HSTS zwiększa ryzyko ataków typu MITM i downgrade HTTPS.

- **Timestamp Disclosure - Unix (2)**  
  Ujawnienie znaczników czasowych w formacie Unix może ułatwiać korelację logów.

- **X-Content-Type-Options Header Missing (17)**  
  Brak nagłówka `nosniff` zwiększa ryzyko wykonywania niebezpiecznych treści.

- **Authentication Request Identified (2)**  
  Endpointy związane z logowaniem zostały zidentyfikowane; wymagana jest kontrola bezpieczeństwa sesji.

- **Modern Web Application (7)**  
  Informacyjny – aplikacja jest typu nowoczesnego SPA/multi-page, wymaga wdrożenia standardowych nagłówków bezpieczeństwa.

- **Re-examine Cache-control Directives (10)**  
  Nagłówki cache mogą pozwalać na niepożądane przechowywanie poufnych danych.

- **Retrieved from Cache (3)**  
  Poufne odpowiedzi mogą być zwracane z cache przeglądarki lub proxy.

- **Session Management Response Identified (5)**  
  Endpointy sesyjne wymagają sprawdzenia TTL sesji, flag Secure, HttpOnly i SameSite.