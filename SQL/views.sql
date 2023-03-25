create or replace view v_emlak as 
select  eml.id, dc.city_name, c.country_name, d.district_name, 
	eml.room, eml.livingroom , dft.floor_type_name ,
	eml.is_furnished, eml.price , eml.sqm_netsqm, eml.maplocation_lat, eml.maplocation_lon,  eml.price/ eml.sqm_netsqm as sqm_price
	FROM public.f_emlak eml
	join d_countries c on c.country_id =eml.country_id
	join d_districts d on d.district_id =eml.district_id
	join d_cities dc on dc.city_id =eml.city_id 
	join d_floor_type dft on dft.floor_type_id =eml.floor_type_id 
	where  eml.price/ eml.sqm_netsqm between 40 and 500
	--limit 100 

create or replace view v_emlak_aggr_by_geo as 	
select   city_id,  x.city_name, x.country_name, x.district_name
,x.is_furnished, cast(avg(sqm_price) as int) sqm_price,count(1) cnt 
from v_emlak x
group by city_id,  x.city_name, x.country_name, x.district_name, x.is_furnished,country_name
order by 1, 3,4	