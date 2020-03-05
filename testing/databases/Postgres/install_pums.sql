CREATE SCHEMA PUMS
	CREATE TABLE PUMS (age int, sex char(2), educ int, race char(2), income float, married boolean )
	CREATE TABLE PUMS_large (PersonID bigint, state int, puma bigint, sex int, age int, educ int, income float, latino boolean, black boolean, asian boolean, married boolean);

\copy PUMS.PUMS FROM '/data/PUMS.csv' CSV;
\copy PUMS.PUMS_large FROM '/data/PUMS_large.csv' CSV;
