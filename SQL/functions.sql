
-- for Postgres version>=15
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
DECLARE  _room_category_id smallint;
DECLARE  _room smallint := room; --have to re-assign to avoid conflicts
DECLARE  _emlak_id int; --id from main fact table
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
	
	  ------ room_category
  
	with src as (select * from (values (_room, livingRoom)) s(room, living_room))
	merge into d_room_category  trg
	using src
		on src.living_room = trg.living_room and src.room = trg.room
	when not matched then
	  insert (room, living_room) values (src.room, src.living_room);
 
    SELECT rc.room_category_id INTO _room_category_id FROM D_Room_Category rc WHERE rc.living_room =livingRoom and rc.room = _room;


	 --
	 WITH src as (select * from (values(load_id, source_emlak_id, age, price, createdate, updateddate, maplocation_lon,maplocation_lat
	 , city_id, country_id, district_id, sqm_netsqm,  floor_count,  is_furnished, _floor_type_id, _room_category_id
	 ))
	 s(load_id, source_emlak_id, age, price, createdate, updateddate, maplocation_lon,maplocation_lat
	 ,city_id, country_id, district_id, sqm_netsqm,  floor_count,  is_furnished, floor_type_id, room_category_id)
	 )
	 MERGE INTO f_emlak as trg
	 using src
		on src.source_emlak_id = trg.source_emlak_id
	 when matched then
	  update set load_id = src.load_id, updateddate = src.updateddate, sqm_netsqm = src.sqm_netsqm
	  , price = src.price,  floor_type_id=src.floor_type_id, room_category_id=src.room_category_id
	 when not matched then
	  insert (load_id, source_emlak_id, age, price, createdate, updateddate, maplocation_lon, maplocation_lat,
	  city_id, country_id, district_id, sqm_netsqm,  floor_count,  is_furnished, floor_type_id, room_category_id)
	  values (src.load_id, src.source_emlak_id, src.age, src.price, src.createdate, src.updateddate
	 ,src.maplocation_lon, src.maplocation_lat, src.city_id, src.country_id, src.district_id
	 ,src.sqm_netsqm, src.floor_count,  src.is_furnished, src.floor_type_id, src.room_category_id);
	
	------f_emlak_details----------
	SELECT fe.id INTO _emlak_id FROM f_emlak fe  where fe.source_emlak_id = source_emlak_id;

	with src as (select * from (values (_emlak_id, detailDescription)) s(id, detailDescription))
	merge into f_emlak_details  trg
	using src
		on src.id = trg.id 
	when matched then
	  update set detailDescription = src.detailDescription
	when not matched then
	  insert (id, detailDescription) values (src.room, src.detailDescription);
	
END
$$;