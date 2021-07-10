# Symulator Skoków Narciarskich - dokumentacja

## Spis klas

- IOSkiJump
- CompetitionManager
- JumpSimulator
- PhysicsSimulator
- JumpResult
- Result
- CompetitionResults
- Hill
- HillProfile
- Jumper

## Opis architektury systemu

System dokonuje symulacji konkursu skoków narciarskich na podstawie danych dostarczonych przez użytkownika. System składa się z klas odpowiedzialnych za interakcję z użytkownikiem (`IOSkiJump`), przebieg konkursu (`CompetitionManager`), symulację skoku (`JumpSimulator`, `PhysicsSimulator`, `Jumper`, `Hill`, `HillProfile`), a także klas służących do obsługi danych z symulacji (`JumpResult`, `Result`, `CompetitionResults`).

## Opis klas

### IOSkiJump

Zadaniem tej klasy jest komunikacja z użytkownikiem poprzez wczytanie plików przez niego dostarczonych. Oprócz tego na podstawie danych z plików, klasa tworzy instancję klasy `CompetitionManager`, która potem służy do przeprowadzenia właściwej symulacji.

Atrybuty:

- `jumpers_data` - dane dotyczące zawodników
- `hills_data` - dane dotyczące skoczni
- `competitions_data` - dane dotyczące konkursu

Metody:

- `read_csv_data(self, file_path)` - wczytuje dane z pliku csv do listy
- `get_hill_data_by_name(self, hill_name)` - uzyskuje dane dotyczące skoczni z `hills_data` na podstawie jej nazwy
- `get_hill_from_hill_data(self, hd)` - tworzy instancję klasy `HillProfile` na podstawie danych z `hills_data`
- `get_jumpers(self)` - tworzy listę instancji `Jumper` na podstawie danych z `jumpers_data`
- `run_competition(self)` - tworzy instancję klasy `CompetitionManager` z danymi uzyskanymi z plików csv

### CompetitionManager

Zadaniem tej klasy jest zarządzanie przeprowadzaną symulacją. Dla każdego zawodnika na liście startowej uruchamia symulację fizyczną skoku, a także losuje seedy potrzebne dla symulatora fizycznego.

Atrybuty:

- `hill`
- `rounds`
- `jumpers`
- `seed`
- `gate`
- `results`
- `simulator`
- `jump_seed_gen`
- `wind_gen`
- `wind_base`
- `wind_bias`

Metody:

- `run_jump(self, jumper, debug=False)` - uruchamia symulację skoku
- `run_competition(self, debug=False)` - uruchamia symulację konkursu (funkcja wykorzystuję `run_jump`)
- `next_jump_seed(self)` - zwraca seed potrzebny do symulacji kolejnego skoku
- `wind_init(self)` - inicjalizuje losowy wiatr
- `get_wind(self, jump_seed)` - zwraca wiatr na podstawia seeda
- `present_results(self)` - zwraca reprezentację tekstową wyników konkursu
- `render_jump(self, fly_x, fly_y, dist, hill)` - zwraca reprezentację graficzną trajektorii lotu skoczka

### JumpSimulator

Atrybuty:

- `hill` - skocznia
- `physics_sim` - instancja klasy `PhysicsSimulator` która wykonuje symulacje fizyczne skoków

Metody:

- `simulate_jump(self, jumper, wind, gate, jump_seed)` - symuluje skok
- `get_aero_coeffs(self, angle)` - oblicza współczynniki aerodynamiczne potrzebne dla symulacji fizycznej
- `get_judges_points(self, jump_seed, normal_speed)` - oblicza noty sędziowskie skoku

### PhysicsSimulator

Klasa jest odpowiedzialna za symulację fizyczną skoku.

Atrybuty:

- `hill` - skocznia na której jest symulowany skok
- `aero_coeffs_fun` - funkcja zwracająca odpowiednie współczynniki aerodynamiczne w zależności od nachylenia trajektorii lotu

Metody:

- `landed(self, pos)` - zwraca prawdę jeśli skoczek wylądował, fałsz gdy skoczek jeszcze leci
- `simulate_inrun(self, gate, inrun_coeff)` - symuluje fazę najazdu
- `simulate_flight(self, v0, takeoff, wind)`- symuluje fazę lotu

### JumpResult

Klasa ta służy do przechowywania danych z symulacji, dodatkowo oblicza punkty za składowe noty, których nie wyznaczył `JumpSimulator`

Atrybuty:

- `speed` - prędkość na progu
- `distance` - odległość
- `self.distance_points` - punkty za odległość
- `gates_diff` róznica belek względem pozycji początkowej
- `gate_points` - punkty za belkę startową
- `wind` - wiatr podczas skoku
- `wind_points` punkty za wiatr
- `judges_points` - noty sędziowskie za skok
- `judges_total` - suma not sędziowskich otrzymanych za skok
- `total_points` - łączna nota za skok

Metody:

- `calculate_judges_points(self)` - oblicza łączną notę sędziowską (odrzuca dwie skrajne i liczy sumę pozostałych)
- `__str__(self)` - reprezentacja tekstowa wyniku za skok

### Result

Klasa ta służy do agregowania wyników skoków oddanych przez jednego skoczka, oprócz tego umożliwiając późniejsze sortowanie listy wyników.

- `athlete` - skoczek
- `total_points` - sumaryczna liczba punktów ze wszystkich skoków
- `rank` - miejsce zajmowane przez skoczka
- `jump_results` - lista wyników skoków

Metody:

- `add_jump(self, jump_result)`- dodaje wynik pojedynczego skoku do listy skoków i aktualizuje wynik
- `__lt__(self, other)`- funkcja porównująca dwa wyniki wg liczby punktów
- `__str__(self)`- reprezenacja tekstowa wyniku skoku

### CompetitionResults

Klasa służąca do zarządzania wynikami całego konkursu.

Atrybuty:

- `hill` - skocznia na której rozgrywany jest konkurs
- `date` - data konkursu
- `competitors` - lista startowa skoczków biorących udział w konkursie
- `results` - wyniki skoczków wg listy startowej
- `sorted_results` - wyniki uporządkowane nierosnąco wzdlęgem noty końcowej

Metody:

- `add_jump_result(self, ind, jmp)` - dodaje skok `jmp` do wyników konkursu
- `sort_results(self)` - porządkuje wyniki na liście `sorted_results`, a także oblicza, które miejsce zajmuje skoczek
- `ordered_results(self)` - generator zwracający wyniki w kolejności od pierwszego do ostatniego wg liczby punktów

### Hill

Klasa zawiera funkcje, które obliczają punkty za usyskaną odległość, belkę, wiatr w zależności od niektórych parametrów skoczni, które nie są wykorzystywane do symulacji fizycznej skoku.

Atrybuty:

- `name`- nazwa skoczni
- `k` - punkt konstrukcyjny skoczni
- `hs` - rozmiar skoczni
- `gate_factor` - współczynnik belki startowej
- `gates_dist` - rozstaw belek startowych na skoczni
- `headwind_fac` - współczynnik wiatru "pod narty"
- `tailwind_fac` - współczynnik wiatru "w plecy"
- `points_meter` - punkty dodawane za każdy metr skoku ponad punkt konstrukcyjny / odejmowane za każdy metr skoku przed punktem konstrukcyjnym
- `points_k` - punkty, które otrzymuje się za osiągnięcie punktu K (120 na skoczniach do lotów narciarskich, 60 na pozostałych)
- `profile` - profil skoczni - instancja klasy `HillProfile`

Metody:

- `get_distance_points(self, distance)` - oblicza punkty za odległość w skoku
- `get_gate_points(self, gates_diff)` - oblicza punkty za belkę startową
- `get_wind_points(self, wind)` - oblicza punkty za wiatr

### HillProfile

Reprezentacja geometryczna profilu skoczni zgodna z normani Międzynarodowej Federacji Narciarskiej (FIS) https://assets.fis-ski.com/image/upload/v1592381507/fis-prod/assets/Construction-Norm_2018-2.pdf, dane dotyczące skoczni można uzyskać z dokumentów homologacji skoczni, które również są dostępne na stronie FIS (homologacja Wielkiej Krokwi w Zakopanem https://medias4.fis-ski.com/pdf/homologations/JP/POL/105_POL_1_Zakopane_HS140.pdf).

Klasa jest również odpowiedzialna za dostarczanie danych dotyczących ukształtowania skoczni potrzebnych do symulacji fizycznej skoku. Klasa oferuje również funkcje, które reprezentują ukształtowanie skoczni, dzięki czemu można stwierdzić, czy skoczek już wylądował.

Atrybuty - różne dane geometryczne skoczni pozwalające odtworzyć jej profil. Opisywanie ich jest mało istotne z punktu widzenia projektu, szczegółowy informacje można uzyskać otwierając pierwszy z linków zamieszczonych wyżej.

Metody:

- `calculate_profile(self)` - dokonuje preprocesingu potrzebnego do dalszych funkcji - wykonuje się w konstruktorze
- `inrun(self, x)` - funkcja reprezentująca najazd skoczni
- `landing_area(self, x)` - funkcja reprezentująca zeskok skoczni
- `get_distance(self, x)` - dystans skoku, który się zakończył w `x`
- `get_tangent(self, x)` - wektor styczny do zeskoku w `x`
- `get_normal(self, x)`- wektor normalny do zeskoku w `x`

### Jumper

Klasa ta służy jako kontener na statystyki skoczka, które to klasa przekształca na rzeczywiste wartości mające wpływ na skok.

Atrybuty:

- `name` - imię i nazwisko skoczka
- `country` - kraj skoczka
- `inrun` - statystyka najazdu skoczka
- `takeoff` - statystyka wybicia skoczka
- `flight` - statystyka lotu skoczka
- `style` - statystyka stylu skoczka

Metody:

- `get_name(self)` - zwraca imię i nazwisko skoczka
- `get_country(self)` - zwraca kraj skoczka
- `get_inrun_coeff(self)` - zwraca współczynniki prędkości najazdu
- `get_takeoff_speed(self)` - zwraca współczynniki prędkości wybicia
- `get_flight_coeffs(self)` - zwraca współczynniki lotu
- `get_style(self)` - zwraca statystykę stylu
- `__str__(self)` - reprezentacja tekstowa zawodnika
