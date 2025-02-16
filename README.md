# F1 Shared Time Trials Apps

## Table of Contents

- [Summary](#summary)
- [Usage](#usage)
  - [Step 1: Install the required modules](#step1)
  - [Step 2: Create Database](#step2)
  - [Step 3: Set Database info](#step3)
  - [Step 4: Create the website](#step4)
  - [Step 5 (Optional): Compile the app](#step5)
- [Known Issues](#issues)

## 🔍 Summary <a id="summary"></a>
This project contains a set of utilities to register Time Trial times from the F1 24 game on a private server, to compare it with whoever shares the same application.

It is composed of 3 main elements:
- Python code, that can be compiled in a shareable exe file
- SQL database that can be imported in your system of choice
- PhP Website to display your records and compare them with friends


## 🔧 Usage <a id="usage"></a>
### <ins>Step 1 : Install the required modules</ins><a id="step1"></a>
Make sure all the required python packages are installed :

```bash
pip install pymysql pyinstaller
``` 
### <ins>Step 2 : Create Database</ins><a id="step2"></a>

Use the racing_db.sql file to import the database structure to your manager. It contains the basic DB structure and all circuits available to F1 24.

### <ins>Step 3: Set Database info</ins><a id="step3"></a>

In *DB_Connection.py*, add your database data.

### <ins>Step 4: Create the website</ins><a id="step4"></a>

If you want to display the data in a fancy way, the repo contains a folder called webpage, which contains a PhP-based website that fetches the data from the DB and displays it. To run it, move the folder to your VPS/Server, making sure to have PhP installed and running, and set the database credentials on *db.php*.

4. Run the app with command 
```bash
python ./Telemetry.py
```

5. 
### <ins>(Optional). Compile the app and share it with other people!</ins><a id="step5"></a>

If you prefer to have an app that runs without having to open a terminal every time, you can easily compile it by running the command

```bash
pyinstaller -F Telemetry.py
```

## Known Issues <a id="issues"></a>
* Times cannot be imported in block. Players need to open every single track with the Telemetry app open to register them
* No way to automatically parse world records
* The app runs on a terminal, and is covered during gameplay
* Sometimes news are not added to the DB
* The best time is the sum of the three sectors and is a redundant info in the DB


