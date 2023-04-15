
alter TABLE F_Emlak 
ADD
    room_category_id SMALLINT   NULL REFERENCES public.D_Room_Category(room_category_id) 
---
    
    
 ; with src as (select distinct room, livingroom from  F_Emlak)
	merge into d_room_category  trg
	using src
		on src.livingroom = trg.living_room and src.room = trg.room
	when not matched then
	  insert (room, living_room) values (src.room, src.livingroom);


UPDATE f_emlak
SET room_category_id = d_room_category.room_category_id
FROM d_room_category
WHERE f_emlak.livingroom = d_room_category.living_room and f_emlak.room = d_room_category.room;

ALTER TABLE f_emlak ALTER COLUMN room_category_id SET NOT NULL


select room_category_id, count(*)  from f_emlak fe group by room_category_id 

-- alter view, alter functions 
alter table f_emlak drop column room
alter table f_emlak drop column livingroom
REINDEX TABLE f_emlak;




	 

	 