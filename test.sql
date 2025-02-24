--Creating Database Shipping Emissions Domestically.
create database ShippingEmissions

---First Table Domestic Shipping By Country Emissions.
CREATE TABLE DomesticShippingByCountry 
( Id int primary key, iso3_Country varchar(10),
Sector varchar (50),Subsector varchar (50),
[Start-Time] datetime,[End-Time] datetime,
Gas decimal(10,2),Emissions_quantity_units decimal(30,20),
Created_date datetime, Modified_Date nvarchar (50)
)


--Comment