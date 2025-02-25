-- creating database 
create database CO2EmissionsInTransport

-- creating tables showing CO2 emissions in shipping both domestically and internationally 
use CO2EmissionsInTransport
go
create table Domestic_Shipping_Country_Emissions1
(
iso3_Country varchar (50),
Subsector varchar (50),
Sector varchar (50),
[Start_Time] datetime,
[End_Time] datetime,
Gas Decimal (10,5),
Emissions_quantity int,
Temporal_Granularity varchar (50))

