--Creating Database Shipping Emissions Domestically.
create database ShippingEmissions

---First Table Domestic Shipping By Country Emissions.
CREATE TABLE DomesticShippingByCountry 
( Id int primary key, iso3_Country varchar(10),
Sector varchar (50),Subsector varchar (50),
[Start-Time] datetime,[End-Time] datetime,
Gas decimal(10,2))

hhh