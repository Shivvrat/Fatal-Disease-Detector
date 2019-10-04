DROP TABLE APP;

CREATE TABLE APP
          (ID INTEGER PRIMARY KEY  AUTOINCREMENT   NOT NULL,
          STATUS             TEXT     NOT NULL,
          TIMESTAMP          TEXT    NOT NULL,
          GEO_LAT   TEXT     NOT NULL,
          GEO_LONG  TEXT     NOT NULL,
          DISEASE    TEXT);
