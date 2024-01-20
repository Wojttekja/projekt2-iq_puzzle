Program main.py rozwiązuje rekurencyjnie puzzle i pokazuje na bieżąco każdy krok
na wykresach z biblioteki matplotlib. Zarówno plansza jak i elementy do użlożenia są
przechowywane jako dwuwymiarowe tablice numpy'owe. 
only_text.py zawiera jedynie funkcję do rozwiązywania i wyświetla tekstowo rozwiązane puzzle.
Służy do testowania wydajności algorytmu bez spowolnienia spowodowanego wyświetlaniem krok po kroku 
procesu układania. 
Czasy ułożenia (only_text.py) poszczególnych planszy:
- plansza2.txt                            (3 elementy)     0:00:00.006053
- plansza3.txt                            (6 elementów)    0:00:01.434290
- more_test_boards/plansza7elementow.txt  (7 elementów)    0:00:34.935832
- more_test_boards/plansza8elementow.txt  (8 elementów)    0:00:23.778502
- more_test_boards/plansza9elementow.txt  (9 elementów)    0:01:17.669171
- more_test_boards/plansza10elementow.txt (10 elementów)   0:02:02.174488

==========================================================================================

IQ puzzle solver with vizualization using matplotlib
Reads boards as numpy two-dimensional arrays
Puzzles are stored as mini numpy arrays
function solve() solves puzzles recursively
only_text.py solves puzzles without graphical showing and prints only final solution, used for testing the algorithm.
Time needed to solve every puzzle:
- plansza2.txt                            (3 puzzles)    0:00:00.006053
- plansza3.txt                            (6 puzzles)    0:00:01.434290
- more_test_boards/plansza7elementow.txt  (7 puzzles)    0:00:34.935832
- more_test_boards/plansza8elementow.txt  (8 puzzles)    0:00:23.778502
- more_test_boards/plansza9elementow.txt  (9 puzzles)    0:01:17.669171
- more_test_boards/plansza10elementow.txt (10 puzzles)   0:02:02.174488

Project made for WDI (Introduction to informatics), my university subject
