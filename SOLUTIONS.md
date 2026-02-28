# Soluții Tasks

Problema **Tasks** cere salariul maxim pe care îl poate obține un inginer alegând ordinea și submulțimea task-urilor pe care le rezolvă. La fiecare alegere: dacă valoarea curentă a task-ului e **pară**, salariul scade cu ea și restul task-urilor cresc cu 1; dacă e **impară**, salariul crește cu ea și restul scad cu 1. Inginerul se poate opri oricând.

---

## brute_force

**Sursă:** `src/brute_force.cpp`

**Idee:** Se generează toate permutările de n elemente și pentru fiecare permutare se simulează ordinea: la fiecare poziție se calculează valoarea curentă a task-ului ales (original + delta), se actualizează salariul conform parității și se actualizează delta (plus = −delta: crește când alegem impar, scade când alegem par). Se păstrează salariul maxim atins pe orice prefix al oricărei permutări.

**Complexitate:** O(n! · n) — n! permutări, fiecare cu n pași.

**Utilizare:** Folosit doar pe n mic (de exemplu n ≤ 10) pentru validarea celorlalte soluții; pe n mare depășește orice limită de timp rezonabilă.

---

## basic_greedy

**Sursă:** `src/basic_greedy.cpp`

**Idee:** Greedy pas cu pas: la fiecare din cei n pași se alege task-ul (neales încă) care maximizează imediat contribuția la salariu: pentru valoarea curentă v, contribuția este +v dacă v e impar și −v dacă v e par. După alegere, task-ul e marcat și valorile curente ale celorlalte se actualizează: +1 dacă am ales par, −1 dacă am ales impar. La fiecare pas se actualizează și salariul maxim pe prefix.

**Complexitate:** O(n²) — n pași, fiecare cu un scan O(n) pentru a alege cel mai bun task și O(n) pentru actualizarea valorilor.

**Utilizare:** Bun ca referință pe teste medii; același algoritm ca optimized_greedy, doar implementat naiv. Folosit ca `good_src` în checker pe teste mari când brute_force nu mai poate rula.

---

## optimized_greedy

**Sursă:** `src/optimized_greedy.cpp`

**Idee:** Același greedy ca basic_greedy: la fiecare pas alegem fie cel mai mic even „curent”, fie cel mai mare odd „curent”, în funcție de care mută oferă câștig mai mare. Implementarea e eficientă: se sortează valorile inițiale și se leagă în două array-uri (odds și evens). După fiecare alegere, delta (efectul cumulat asupra valorilor rămase) se schimbă, deci paritatea „curentă” se invarte: se folosește variabila `carry` (= −delta) și la fiecare pas se face swap între ce considerăm „odds” și „evens”. Se mențin doar pointeri și size-uri pe segment; cel mai mic even e la începutul segmentului de evens, cel mai mare odd la sfârșitul segmentului de odds, fără scan complet.

**Complexitate:** O(n log n) pentru sortare + O(n) pentru cei n pași (operații O(1) pe segment).

**Utilizare:** Soluția de concurs pentru n mare (până la 10⁶); același răspuns ca basic_greedy, dar în timp liniar-logaritmic.
