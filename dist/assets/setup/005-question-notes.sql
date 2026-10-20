-- Run once in this site's Supabase SQL Editor. Safe to run again.
begin;
-- Also register the 20 challenge IDs if the previous migration was skipped.
insert into public.pp_question_catalog(id,kind,stage)
select v.stage||'-C'||lpad(v.chapter::text,2,'0')||'-R'||lpad(g.n::text,2,'0'),'original',v.stage
from (values ('P3',6,40),('P3',7,35),('P2',7,35)) as v(stage,chapter,last_no)
cross join lateral generate_series(31,v.last_no) as g(n)
on conflict(id) do nothing;
create table if not exists public.pp_question_notes (
 user_id uuid not null references public.pp_profiles(id) on delete cascade,
 question_id text not null references public.pp_question_catalog(id),
 note text not null default '' check (char_length(note)<=10000),
 version bigint not null default 0,
 updated_at timestamptz not null default now(),
 primary key(user_id,question_id)
);
alter table public.pp_question_notes enable row level security;
revoke all on public.pp_question_notes from public,anon,authenticated;
grant select on public.pp_question_notes to authenticated;
drop policy if exists pp_self_notes on public.pp_question_notes;
create policy pp_self_notes on public.pp_question_notes for select to authenticated using(user_id=auth.uid());

create or replace function public.pp_notes_snapshot() returns jsonb
language plpgsql security definer set search_path=pg_catalog as $notes$
declare uid uuid:=auth.uid();
begin
 if uid is null then raise sqlstate 'PT401' using message='请先登录'; end if;
 return coalesce((select jsonb_agg(jsonb_build_object('question_id',n.question_id,'note',n.note,'version',n.version,'updated_at',n.updated_at)) from public.pp_question_notes n where n.user_id=uid),'[]'::jsonb);
end;
$notes$;

create or replace function public.pp_save_note(p_question_id text,p_note text,p_base_version bigint) returns jsonb
language plpgsql security definer set search_path=pg_catalog as $notes$
declare uid uuid:=auth.uid(); r public.pp_question_notes;
begin
 if uid is null then raise sqlstate 'PT401' using message='请先登录'; end if;
 if p_note is null or char_length(p_note)>10000 or p_base_version is null or p_base_version<0 then raise sqlstate 'PT400' using message='备注最多10000字，版本须有效'; end if;
 if p_question_id is null or not exists(select 1 from public.pp_question_catalog where id=p_question_id) then raise sqlstate 'PT400' using message='题号尚未登记，请联系管理员'; end if;
 insert into public.pp_question_notes(user_id,question_id) values(uid,p_question_id) on conflict do nothing;
 select * into r from public.pp_question_notes where user_id=uid and question_id=p_question_id for update;
 if r.version<>p_base_version then raise sqlstate 'PT409' using message='另一设备已修改备注；请对比云端内容后选择保留哪一份'; end if;
 update public.pp_question_notes set note=p_note,version=version+1,updated_at=now() where user_id=uid and question_id=p_question_id returning * into r;
 return jsonb_build_object('question_id',r.question_id,'note',r.note,'version',r.version,'updated_at',r.updated_at);
end;
$notes$;
revoke all on function public.pp_notes_snapshot(),public.pp_save_note(text,text,bigint) from public,anon,authenticated;
grant execute on function public.pp_notes_snapshot(),public.pp_save_note(text,text,bigint) to authenticated;
commit;
