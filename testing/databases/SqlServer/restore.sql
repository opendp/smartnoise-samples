CREATE DATABASE [Devices];
GO

USE Devices;
GO

CREATE SCHEMA Telemetry
	CREATE TABLE Crashes (Region varchar(50), Temperature double precision, Building varchar(20), DeviceID int, Refurbished bit, Crashes int)
	CREATE TABLE Census (DeviceID int, [OEM] varchar(50), Memory varchar(50), [Disk] bigint )
	CREATE TABLE Rollouts (DeviceID int, RolloutID int, [StartTrial] datetime, [EndTrial] datetime, [TrialGroup] int);

GO

CREATE DATABASE PUMS;
GO

USE PUMS;
GO

CREATE SCHEMA PUMS
	CREATE TABLE PUMS (age int, sex char(2), educ int, race char(2), income float, married bit )
	CREATE TABLE PUMS_large (PersonID int, state int, puma int, sex int, age int, educ int, income float, latino bit, black bit, asian bit, married bit);
GO



CREATE DATABASE [Legacy];
GO

USE Legacy;
GO


CREATE TABLE Crashes (Region varchar(50), Temperature double precision, Building varchar(20), [DeviceID] int, Refurbished bit, Crashes int);
GO
CREATE TABLE Census ([DeviceID] int, [OEM] varchar(50), Memory varchar(50), [Disk] bigint );
GO
CREATE TABLE [Rollouts] ([DeviceID] int, RolloutID int, [StartTrial] datetime, [EndTrial] datetime, [Group] int);
GO
