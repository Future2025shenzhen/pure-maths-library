-- Append challenge IDs; existing accounts, records and permissions are unchanged.
insert into public.pp_question_catalog(id,kind,stage) values
('P3-C06-R31','original','P3'),
('P3-C06-R32','original','P3'),
('P3-C06-R33','original','P3'),
('P3-C06-R34','original','P3'),
('P3-C06-R35','original','P3'),
('P3-C06-R36','original','P3'),
('P3-C06-R37','original','P3'),
('P3-C06-R38','original','P3'),
('P3-C06-R39','original','P3'),
('P3-C06-R40','original','P3'),
('P3-C07-R31','original','P3'),
('P3-C07-R32','original','P3'),
('P3-C07-R33','original','P3'),
('P3-C07-R34','original','P3'),
('P3-C07-R35','original','P3'),
('P2-C07-R31','original','P2'),
('P2-C07-R32','original','P2'),
('P2-C07-R33','original','P2'),
('P2-C07-R34','original','P2'),
('P2-C07-R35','original','P2')
on conflict(id) do nothing;
