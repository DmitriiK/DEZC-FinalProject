------



-- call pr_calc_emlak_data()
CREATE or REPLACE PROCEDURE pr_calc_emlak_data()
LANGUAGE plpgsql
AS $$
BEGIN
 with most_recent_load as (select  fl2.load_id  from f_loads fl2 where fl2.is_full and fl2.status =1 order by fl2.load_id desc limit 1)
 ,not_recent_load as (select  eml.id  
	from  public.f_emlak eml	
	cross join most_recent_load mrl
	where eml.load_id < mrl.load_id)
    update f_emlak set is_most_recent_load = false 
   		from not_recent_load where not_recent_load.id=f_emlak.id;	
END
$$;

