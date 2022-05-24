CREATE TABLE IF NOT EXISTS public.test_results
(
    polarity integer,
    “text” text ,
    new_date text,
    “length” integer,
    “label” double precision NOT NULL,
    token_text text[],
    prediction double precision NOT NULL
)

select * from public.test_results;