Change log
----------

- **0.0.8** 2017/12/28

    - Data base update. Suppress unique index on sensor id in location.
      Please run V007to008.sql available on http://static.frkb.fr/wdwapp
      
    Corrections :
    - When new sensor is detected save first data received.
    - Internal Server Error after lost MySql connection due to interactive
      timeout.
      Resolved by adding pool_pre_ping=True to create_engine.

- **0.0.7** 2017/12/28

    - Data base update. Add rank and grah color to location.
      Please run V006to007.sql available on http://static.frkb.fr/wdwapp
    - Secure humidity reading. Cannot be below 1 or upper 100.
    - Added detail view of last 24h data for a location.

- **0.0.6** 2017/12/26

    - Beginning with the webserver.
      A first page with last datas is available (in french sorry).
    - Data base update. Add long description to server.
      Please run V004to005.sql available on http://static.frkb.fr/wdwapp
    - Removed tests.

- **0.0.4** 2017/12/25

	- Remove return value.
    - Change logging system to manage different levels (debug, error, warning,
      etc.). In this way, for example, warnings can be send by mail from cron.
      This implies mail option from log() have been removed.
    - Suppress of backup file. Replaced by sensor_data table.
      This table is indexed with sensor ID and timestamp so it is easier to
      re-process data for a new sensor (re-process part need to be written).

- **0.0.3** 2017/12/22

	- Rounding results to avoid truncate warning during database update.
    - Avoid to insert already existing weather data.

- **0.0.1** 2017/12/21

	First version.
