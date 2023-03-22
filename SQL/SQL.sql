CREATE TABLE F_LOADS
(
load_Id  INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
dt_start TIMESTAMP NOT NULL,
dt_end TIMESTAMP  NULL,
rows_processed INT
)
CREATE TABLE D_Cities
(
	city_id INT NOT NULL PRIMARY KEY,
	city_name VARCHAR(50),
	load_id INT NOT NULL REFERENCES F_LOADS(load_id)
)
--
create TABLE D_Countries
(
	country_id INT NOT NULL PRIMARY KEY,
	country_name VARCHAR(50),
	load_id INT NOT NULL REFERENCES F_LOADS(load_id)
)
--
CREATE TABLE D_Districts
(
	district_id INT NOT NULL PRIMARY KEY,
	district_name VARCHAR(50),
	LOAD_ID INT NOT NULL REFERENCES F_LOADS(load_id)
)

-- DROP TABLE IF EXISTS public.d_floor_type;

CREATE TABLE  public.d_floor_type
(
    floor_type_id INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    load_id  INT NOT NULL REFERENCES F_LOADS(load_id),
    floor_type_name character varying(50),
    floor_number INT NULL, --supposed to be defined manually by translation
    UNIQUE(floor_type_name)
)

CREATE TABLE F_Emlak
(
    id  INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    load_id INT NOT NULL REFERENCES F_LOADS(load_id),
    source_emlak_id INT NOT NULL,
    age INT,
    price INT NOT NULL,
    createDate TIMESTAMP NOT NULL,
    updatedDate TIMESTAMP,
    mapLocation_lon NUMERIC(18,16),
    mapLocation_lat NUMERIC (18,16),
    city_id INT NOT NULL REFERENCES public.D_Cities(city_id),
    country_id INT  NOT NULL REFERENCES public.D_Countries(country_id),
    district_id  INT  NOT NULL REFERENCES public.D_Districts(district_id),
    sqm_netSqm INT,
    room INT,
    LivingRoom INT,
    floor_count INT,
    detailDescription  VARCHAR(255),
    is_furnished BOOLEAN,
    is_gaz BOOLEAN,
    floor_type_id INT NULL REFERENCES public.d_floor_type(floor_type_id)
    UNIQUE(source_emlak_id)
)

-- drop PROCEDURE pr_merge_emlak_data
CREATE or REPLACE PROCEDURE pr_merge_emlak_data (
	load_id integer,
	source_emlak_id integer,
	age INT,
	price NUMERIC(10,2),
	createDate TIMESTAMP,
	updatedDate TIMESTAMP	,
	mapLocation_lon NUMERIC(18,16),
	mapLocation_lat NUMERIC (18,16),
	city_id INT,
	city_name VARCHAR(50),
	country_id INT ,
	country_name VARCHAR(50),
	district_id  INT,
	district_name VARCHAR(50),
	sqm_netSqm NUMERIC(6,2),
	room INT,
	livingRoom INT,
	floor_count INT,
	floor_type VARCHAR(50),
	detailDescription  VARCHAR(255),
	is_furnished Boolean
	/**/
)
LANGUAGE plpgsql
AS $$
DECLARE  _floor_type_id int;
BEGIN
	with src as (select * from (values (city_id, city_name ,load_id)) s(city_id, city_name,load_id))
	merge into D_Cities trg
	using src
		on src.city_id = trg.city_id
	when matched then
	  update set city_name = src.city_name
	when not matched then
	  insert (city_id, city_name, load_id) values (src.city_id, src.city_name, src.load_id);
	--
	with src as (select * from (values (district_id, district_name ,load_id)) s(district_id, district_name, load_id))
	merge into D_Districts  trg
	using src
		on src.district_id = trg.district_id
	when matched then
	  update set district_name = src.district_name
	when not matched then
	  insert (district_id, district_name, load_id) values (src.district_id, src.district_name, src.load_id);
	--
	with src as (select * from (values (country_id, country_name ,load_id)) s(country_id, country_name, load_id))
	merge into D_Countries  trg
	using src
		on src.country_id = trg.country_id
	when matched then
	  update set country_name = src.country_name
	when not matched then
	  insert (country_id, country_name, load_id) values (src.country_id, src.country_name, src.load_id);
	 --
	INSERT INTO d_floor_type(floor_type_name, load_id)
	SELECT floor_type,load_id WHERE floor_type IS NOT NULL
	ON     CONFLICT DO NOTHING;

    SELECT ft.floor_type_id INTO _floor_type_id FROM d_floor_type ft WHERE ft.floor_type_name =floor_type;

	 --
	 WITH src as (select * from (values(load_id, source_emlak_id, age, price, createdate, updateddate, maplocation_lon,maplocation_lat
	 , city_id, country_id, district_id, sqm_netsqm, room, livingRoom, floor_count, detaildescription, is_furnished, _floor_type_id
	 ))
	 s(load_id, source_emlak_id, age, price, createdate, updateddate, maplocation_lon,maplocation_lat
	 ,city_id, country_id, district_id, sqm_netsqm, room, livingRoom, floor_count, detaildescription, is_furnished, floor_type_id)
	 )
	 MERGE INTO f_emlak as trg
	 using src
		on src.source_emlak_id = trg.source_emlak_id
	 when matched then
	  update set load_id = src.load_id, updateddate = src.updateddate, sqm_netsqm = src.sqm_netsqm
	  , price = src.price, detaildescription = src.detaildescription, floor_type_id=src.floor_type_id
	 when not matched then
	  insert (load_id, source_emlak_id, age, price, createdate, updateddate, maplocation_lon, maplocation_lat,
	  city_id, country_id, district_id, sqm_netsqm, room, livingRoom, floor_count, detaildescription, is_furnished, floor_type_id)
	  values (src.load_id, src.source_emlak_id, src.age, src.price, src.createdate, src.updateddate
	 ,src.maplocation_lon, src.maplocation_lat, src.city_id, src.country_id, src.district_id
	 ,src.sqm_netsqm, src.room, src.livingRoom, src.floor_count, src.detaildescription, src.is_furnished, src.floor_type_id);
END
$$;


