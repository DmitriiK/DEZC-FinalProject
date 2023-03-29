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

CREATE TABLE  public.f_emlak_calc -- extension table with calculations
(
    id  INT NOT NULL  PRIMARY KEY REFERENCES F_Emlak(id),   
    dist_to_sea INT NOT NULL --distance to sea border
)



