# iotaWayBack
`iotaWayBack` is a tool for compiling a SQL database based on confirmed transactions, from past IOTA DBs.

In addition, it's a tool to document the process I did, to create my copy of this SQL DB - a continuous database of confirmed transaction from **Oct. 4 2016 - Aug. 8 2017**.

**if you only want to search my DB, without building your own - jump to `4.`** 
### from IRI to SQL:
 #### 1. obtaining past IOTA DBs:
 All pre-snapshot dbs can be found here: [http://alon-e.com/IOTA_DBs](http://alon-e.com/IOTA_DBs).
 
 More information on the DB collection process can be found [here](https://docs.google.com/spreadsheets/d/1cnSlLjfyHfpjXAzwOEpAk1w1zGc0dYP_mmATuctqN0s/edit#gid=0).  
 *credit to @lobeto, who reached out to veteran IOTA users to complete the missing DBs. 
 
 #### 2. traversing confirmed transactions & dumping raw trytes:
 in each IOTA DB you will find an `iri.jar` file, matching the version used back when the database was used.
 
 and a `start.bat` file with an appropriate command to spin-up the node.
 
 for each IOTA DB you want to dump:
 1. start IRI node.
 2. run `python traverse.py`.
 3. (stop IRI node)
 
 _this will create a `.dmp` file with `<hash>,<raw_trytes>` for each IRI version, which will be parsed by the next stage._
 
 _each `IOTA_DB` zip also contains the `.dmp` file computed on by me, if you want to skip this stage._
 
 #### 3. importing transaction into database:
 _after completing all IOTA DB dumps continue to importing_
 
 You have a choice of `DBEngine` between: `sqlite` & `MySQL`.
 - `sqlite` is a local DB, no setup required.
 - `MySQL` requires running a server, but is more performant.
 

 _given the size of the DB (~4M entries), I went with MySQL.
 as MySQL requires a server, I assume if you chose this option, you know how to setup a schema (`iotaWayBack`) & manage user privileges (user, password in `parse_and_store.py`)._
 
 1. run `pip install -e .`
 2. set `DBEngine` in `parse_and_store.py` according to your DB Engine decision above.
 3. (if you have the `.dmp` files in a different folder, set `folder` in `parse_and_store.py` accordingly.)
 4. run `python parse_and_store.py`
 
 _this will create a table `transactions` that has each confirmed transaction with parsed fields._
 
  #### 4. using the SQL DB:
_I have a version of this process running. contact me on iota's slack, if you want to skip all the above steps & just access the data._
 
 now you can open the SQL DB with your favorite client.
 my GUI favorites:
 - `sqlite` DB browser for SQLite - http://sqlitebrowser.org/
 - `MySQL` MySQL Workbench - https://dev.mysql.com/downloads/workbench/
 
 or the packaged CLI tools: `sqlite`, `mysql`. 
 
 
 #### Example queries:
```
SELECT * FROM iotaWayBack.transactions WHERE hash='XTEZNQAGBATWVOMEPVEEIGHR9HUBNAXHXAIJ9PUCGSINPGVNCEUXSZV9GNAYDVXVVTYKVIMWVEZW99999'; // get transaction details by hash
```

```
SELECT * FROM iotaWayBack.transactions WHERE address='YOURADDRESS'; // get all the transations associated with a given address.
```

```
SELECT count(*) FROM (SELECT DISTINCT address FROM iotaWayBack.transactions GROUP BY address) as A; // count all unique address in IOTA.
```

```
SELECT * FROM iotaWayBack.transactions WHERE timestampDate>'2017/08/05' AND timestampDate<'2017/08/06'; // get all transaction in a given time window.
```
