-- Run only in the Supabase SQL Editor as project owner, after registering your own account.
-- Replace the string below with YOUR nickname. Never automatically promote the first registrant.
insert into public.pp_admins(user_id)
select id from public.pp_profiles
where nickname_key=lower(normalize('替换为你的管理员昵称',NFKC))
on conflict do nothing;
-- Confirm that exactly your intended account appears:
select p.nickname,p.id from public.pp_profiles p join public.pp_admins a on a.user_id=p.id;
