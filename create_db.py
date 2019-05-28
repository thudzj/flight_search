import sqlite3
conn = sqlite3.connect('flights.db')
cursor = conn.cursor()

items = {
	"id": "varchar(100) primary key",
	ItinerarDate	date,
	Airline			varchar(100),
	AirlineCode		varchar(100),
	FlightNumber	varchar(20),
	FlightNumberS	varchar(20),
	Aircraft		varchar(50),
	AircraftSize	char(2),
	AirportTax		decimal(10,2),
	FuelOilTax		decimal(10,2),
	FromCity		varchar(50),
	FromCityCode	varchar(10),
	FromAirport		varchar(50),
	FromTerminal	varchar(20),
	FromDateTime	datetime,
	ToCity			varchar(50),
	ToCityCode		varchar(10),
	ToAirport		varchar(50),
	ToTerminal		varchar(20),
	ToDateTime		datetime,
	DurationHour	int,
	DurationMinute	int,
	Duration		varchar(20),
	Currency		varchar(10),
	TicketPrices	decimal(10,2),
	Discount		decimal(4,2),
	PunctualityRate	decimal(4,2),
	AircraftCabin	char(1),
	InsertDate		datetime default(getdate())
}

cursor.execute('create table flights (id varchar(100) primary key, name varchar(20))')
#cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')cursor.close()
conn.commit()
conn.close()