# Mini-Eksamen-DDU
## Digital Design
### Gruppe: Anders, Simon og Marcus Hansen fra L 3d2 og Adam fra L 3i
### Deadline: ??/??-??:??
### Navn på hjemmeside/projekt: 


### Hvordan kører man hjemmesiden lokalt?

#### Først og fremmest er der noget man skal installere

Installer Python på dit operativsystem, sørg for at du har adgang til
og kan bruge python3 kommandoen i din terminal/kommandoprompt!

Alle de ting du bliver præsenteret for er noget du skal gøre i din terminal/kommandoprompt

Først skal du clone det her repository:
`git clone https://github.com/gulfurs/Mini-Eksamen-DDU`

Det første du skal gøre er at lave et virtuelt python miljø i samme mappe som det klonet repository!:
`Python3 -m pip venv env`

#### Windows
Hvis du er på Windows så gør følgende:

Tilføje følgende linjer til activate.bat filen der befinder sig i følgende mappe sti: ./env/Scripts/
`set FLASK_ENV=development`
`set FLASK_APP=main.py`

Du bliver nok nødt til at [installere postgressql](https://www.postgresql.org/download/windows/) og tilføje den til din "path" ligesom med Python

Nu skal du aktivere dit nye python miljø:
Skriv `activate.bat` inden i ./env/Scripts/ og tryk enter

Derefter skal du installere alle de pakker der står i requirements.txt filen i det her repository.
**du** skal **stadig** sørge for at have python miljøet aktiveret!:
`pip3 install -r requirements.txt`

#### MacOS/Linux
Hvis du er på MacOS eller Linux så gør følgende:

Tilføje følgende linjer til activate filen der befinder sig i følgende mappe sti: ./env/bin/
`export FLASK_ENV=development`
`export FLASK_APP=main.py`:

Nu skal du aktivere dit nye python miljø:
Skriv `source activate` inden i ./env/bin/ og tryk enter

Derefter skal du installere alle de pakker der står i requirements.txt filen i det her repository.
**du** skal **stadig** sørge for at have python miljøet aktiveret!:
`pip3 install -r requirements.txt`


#### Hvordan kører jeg hjemmesiden så?
Det er meget simpelt du skal bare befinde dig i rodmappen af dette repository og eksekvere følgende kommando:
**du** skal **stadig** sørge for at have python miljøet aktiveret!:

`flask run`

### Hvordan forbinder man til databasen (Skal kun bruge i forbindelse med udvikling af hjemmesiden)?
Du skal først lige installere heroku CLI
Så skal du logge ind ved at eksekvere følgende kommando: `heroku login`
Derefter når du er logget ind så eksekver følgende kommando: `heroku pg:psql postgresql-graceful-82804 --app school-site-project`

### Alle links:

[Burndownchart](https://docs.google.com/spreadsheets/d/12GrolWbVKDg1Wu-nvA1gK3bWTYi4yTNMDA7evywdAyM/edit?usp=sharing)

[Test og møde log](https://docs.google.com/document/d/1EtqgZI1tlutKvl88_4Fm8d4sHtB1s6ItvU_p9tvqYg4/edit?usp=sharing)

[Rapport](https://docs.google.com/document/d/1D4JML7Tyzi70eCvyhFqcaqu-nzUixWOj3uAb32aINHo/edit?usp=sharing)

[Kvalitativ interview](https://docs.google.com/document/d/1ZcOceFuOrCk-WHEqFYpmXqh5PTlM2hQL2-aBG_DJ60g/edit#heading=h.jan5098veqpe)

