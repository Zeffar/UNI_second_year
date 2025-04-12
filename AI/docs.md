P1

Euristica aleasă este distanța Manhattan, calculată ca abs(x1 - x2) + abs(y1 - y2), unde (x1, y1) și (x2, y2) sunt coordonatele a două noduri. 
Această euristică este admisibilă deoarece, în acest graf specific, costul fiecărei muchii este exact egal cu distanța Manhattan dintre coordonatele nodurilor conectate de acea muchie. 
Prin urmare, costul oricărui drum din graf este egal cu suma distanțelor Manhattan ale muchiilor de pe acel drum. 
Deoarece distanța Manhattan directă dintre nodul de start și nodul scop reprezintă cea mai mică sumă posibilă a distanțelor Manhattan (și deci a costurilor) necesară pentru a ajunge la scop, 
valoarea euristicii nu va supraestima niciodată costul real al celui mai scurt drum, asigurând astfel admisibilitatea.


P2
Funcția heuristică utilizată pentru evaluarea stărilor în jocul Țintar (Nine Men's Morris) este concepută pentru a estima cât de favorabilă este o configurație a tablei pentru jucătorul MAX ('x'). 
Aceasta combină mai mulți factori considerați esențiali pentru succes în acest joc:

    Diferența de Piese: Cel mai fundamental factor este numărul de piese pe tablă. A avea mai multe piese decât adversarul oferă mai multe opțiuni strategice și un avantaj material direct. 
    Pierderea pieselor sub pragul de 3 duce la înfrângere. Euristica acordă un scor pozitiv pentru fiecare piesă în plus față de adversar.

    Morile Formate: Formarea unei mori (trei piese în linie) este crucială, deoarece permite eliminarea unei piese a adversarului. 
    Euristica acordă o pondere semnificativă diferenței dintre numărul de mori formate de 'x' și cele formate de 'o', reflectând avantajul strategic major obținut.

    Morile Potențiale: O linie care conține două piese proprii și un spațiu liber reprezintă o amenințare iminentă de a forma o moară. 
    Controlul acestor "mori potențiale" este important atât ofensiv (pentru a crea oportunități), cât și defensiv (pentru a bloca adversarul). 
    Euristica numără aceste configurații și le acordă o pondere pozitivă, deși mai mică decât morile complete.

    Mobilitatea: Numărul de mutări valide disponibile pentru un jucător (fie plasări în prima fază, fie mutări în a doua fază) reflectă flexibilitatea sa strategică. 
    Un jucător cu mobilitate mai mare poate reacționa mai ușor la acțiunile adversarului și poate iniția atacuri. Blocarea completă a mutărilor adversarului duce la victorie. 
    Euristica include diferența de mobilitate ca un factor pozitiv.

    Piesele Blocate (în faza de mutare): O piesă care nu are nicio poziție adiacentă liberă este blocată și inutilă temporar. 
    Euristica penalizează ușor stările în care jucătorul are piese blocate și recompensează stările în care adversarul are piese blocate.

Acești factori sunt combinați printr-o sumă ponderată, unde ponderile reflectă importanța relativă a fiecărui aspect (de exemplu, morile formate au o pondere mai mare decât mobilitatea). 
De asemenea, euristica tratează distinct fazele jocului (plasare vs. mutare) și include verificări pentru stările terminale (victorie/înfrângere), 
returnând valori foarte mari sau foarte mici pentru a ghida corect algoritmii Minimax/AlphaBeta. Această abordare multi-factorială oferă o estimare robustă a valorii unei stări de joc.

P3
În abordarea noastră simplificată, inspirată de Rețelele Bayesiene, nu construim explicit o rețea cu tabele de probabilități condiționale (CPT-uri), 
deoarece acest lucru ar necesita date de antrenament sau definirea manuală complexă a sute de probabilități. 
În schimb, folosim funcția heuristică existentă ca un proxy pentru scorul pe care o Rețea Bayesiană l-ar atribui unei stări. 
Această funcție combină liniar diverse caracteristici (features) ale stării de joc, iar ponderile asociate fiecărei caracteristici reflectă importanța relativă 
sau puterea de influență a acelei caracteristici asupra "probabilității" ca starea respectivă să fie favorabilă jucătorului 'x'.

Alegerea ponderilor se bazează pe cunoștințe despre strategia jocului Țintar:

    w_mill = 60 (Diferența de Mori): Aceasta are cea mai mare pondere. 
    Formarea unei mori este evenimentul cel mai important strategic, deoarece permite capturarea unei piese adverse și poate schimba dramatic cursul jocului. 
    O diferență pozitivă mare în numărul de mori indică un avantaj substanțial. Această pondere mare reflectă influența directă și puternică a morilor asupra câștigării jocului.

    w_piece = 25 (Diferența de Piese): Avantajul material (a avea mai multe piese) este fundamental. Oferă mai multe opțiuni, control asupra tablei și rezistență la capturi. 
    Este al doilea cel mai important factor, de aceea are o pondere semnificativă, dar mai mică decât morile, deoarece o moară poate anula rapid un avantaj numeric mic.

    w_potential = 7 (Diferența de Mori Potențiale): Controlul liniilor cu două piese proprii și un spațiu liber ("aproape mori") este important pentru a crea amenințări viitoare și a restricționa adversarul. 
    Este un factor strategic relevant, dar efectul său nu este la fel de imediat sau garantat ca o moară completă, deci ponderea este moderată.

    w_blocked = 3 (Diferența de Piese Blocate): A avea piese blocate reduce mobilitatea și eficiența. 
    Blocarea pieselor adversarului este un avantaj. Factorul are o pondere mică, deoarece situațiile de blocaj total sunt mai rare decât alte avantaje, dar contribuie la evaluarea fină a poziției în faza de mutare.

    w_mobility = 2 (Diferența de Mobilitate): Flexibilitatea de a muta piesele este utilă, permițând repoziționarea și exploatarea oportunităților. 
    O mobilitate mai mare este în general bună. Are cea mai mică pondere, deoarece numărul brut de mutări nu surprinde întotdeauna calitatea acelor mutări 
    (o singură mutare care formează o moară este mai valoroasă decât multe mutări pasive).

Aceste ponderi transformă caracteristicile observate ale stării de joc într-un scor unic, care aproximează cât de "bună" este starea respectivă. 
Abordarea selectează mutarea care duce la starea imediat următoare cu cel mai mare scor (cea mai mare "probabilitate" estimată de a fi bună), 
acționând ca un agent greedy bazat pe această evaluare inspirată de principiile combinării dovezilor din Rețelele Bayesiene.
