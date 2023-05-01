create or replace view v_room_category as 
select rc.room_category_id, rc.room, rc.living_room,
	concat(rc.room, '+', rc.living_room) as room_plus_living_room,
	case when rc.room>3 then '>4+..' else concat(rc.room, '+', rc.living_room) end as room_category
from  d_room_category rc
--


--select * from v_emlak
create or replace view v_emlak as 
select  eml.id, 
	eml.createdate, eml.updateddate, fl.dt_start as last_load_date,
	eml.is_most_recent_load,
  	eml.city_id,  dc.city_name
   ,eml.country_id, c.country_name
   ,eml.district_id,  d.district_name, 
	rc.room,  rc.living_room as livingroom , dft.floor_type_name , eml.floor_count,
	cast(eml.is_furnished as int)  as is_furnished, 
	eml.price , eml.sqm_netsqm, eml.maplocation_lat, eml.maplocation_lon,
	eml.age, 
	cast(1.0*ec.dist_to_sea/1000 as decimal(6,1)) as dist_to_sea,
	calc.sqm_price
	,eml.room_category_id, rc.room_category 
	,case when eml.is_furnished then calc.sqm_price else 0 end sqm_price_furnished
	,case when eml.is_furnished then 1 else 0 end cnt_furnished
	,case when not eml.is_furnished then calc.sqm_price else 0 end sqm_price_not_furnished
	,case when not eml.is_furnished then 1 else 0 end cnt_not_furnished
	from  public.f_emlak eml
	join d_countries c on c.country_id =eml.country_id
	join d_districts d on d.district_id =eml.district_id
	join d_cities dc on dc.city_id =eml.city_id 
	join d_floor_type dft on dft.floor_type_id =eml.floor_type_id 
	join f_loads fl  on fl.load_id =eml.load_id
	left join v_room_category rc on rc.room_category_id=eml.room_category_id
	left join public.f_emlak_calc ec  on eml.id=ec.id 
	,
	lateral (select eml.price/eml.sqm_netsqm as sqm_price) calc
	where  eml.price/ eml.sqm_netsqm between 40 and 500
	--and eml.Id=11030
--
create view v_is_furnitured as
SELECT * FROM (VALUES (false, 'empty'), (true, 'furnitured')) AS t (is_furnitured,n_is_furnitured);
	 

	--
DROP view v_aggr_all

create or replace view v_aggr_all as 
with aggr_eml as (
	select count(1) as cnt_all from f_emlak eml
)
,loads as (
select fl2.load_id , fl2.items_processed, fl2.dt_start
from f_loads fl2, aggr_eml
where fl2.is_full and fl2.status =1 order by fl2.load_id desc limit 1
)
select * from aggr_eml, loads

	