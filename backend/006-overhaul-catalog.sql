-- Register existing overhaul IDs, including historical withdrawn IDs.
-- Run as database owner; no account records or permissions are changed.
insert into public.pp_question_catalog(id,kind,stage) values
('P1-C04-R31','original','P1'),
('P1-C04-R32','original','P1'),
('P1-C04-R33','original','P1'),
('P1-C04-R34','original','P1'),
('P1-C04-R35','original','P1'),
('P1-C04-R36','original','P1'),
('P1-C07-R31','original','P1'),
('P1-C07-R32','original','P1'),
('P1-C07-R33','original','P1'),
('P1-C07-R34','original','P1'),
('P1-C07-R35','original','P1'),
('P1-C07-R36','original','P1'),
('P1-C07-R37','original','P1'),
('P1-C07-R38','original','P1'),
('P1-C09-R31','original','P1'),
('P1-C09-R32','original','P1'),
('P1-C09-R33','original','P1'),
('P1-C09-R34','original','P1'),
('P1-C09-R35','original','P1'),
('P1-C09-R36','original','P1')
on conflict(id) do nothing;
