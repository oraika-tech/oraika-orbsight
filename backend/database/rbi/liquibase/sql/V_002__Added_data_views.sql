--liquibase formatted sql

--changeset girish:rbi_ddl_002
create view processed_data_view_v1 as
select
	rd.event_time,
	-- ids ---------
	rd.identifier as raw_data_id,
    pd.identifier as processed_data_id,
    rd.reference_id,
    rd.data ->>'conversation_id' as conversation_id,
    -- entity info -------
    pd.observer_type,
    rd.entity_name,
    rd.regulated_entity_type,
    -- message info ------
    (case
        when pd.observer_type = 'Twitter' then (rd.data->>'author_info')::json->>'username'
        when pd.observer_type = 'Android' then rd.data->>'userName'
        when pd.observer_type = 'iOS' then rd.data->>'author_name'
    end) as author_name,
    (case
        when pd.observer_type = 'Android' then rd.data->>'score'
        when pd.observer_type = 'iOS' then rd.data->>'rating'
    end) as rating,
    pd.emotion,
    rd.raw_text,
    -- Text meta
    md5(rd.raw_text) as text_hash,
    pd.text_lang,
    pd.text_length,
    (case
        when pd.observer_type = 'Twitter' then rd.data->>'tweet_url'
    end) as url,
    -- analysis data --------
    (array[]::text[]
    || case when service is not null then array['service'] end
    || case when payment is not null then array['payment'] end
    || case when transfer is not null then array['transfer'] end
    || case when account_type is not null then array['account_type'] end
    || case when card is not null then array['card'] end
    || case when identification is not null then array['identification'] end
    || case when security is not null then array['security'] end
    || case when currency is not null then array['currency'] end
    || case when stock_market is not null then array['stock_market'] end
    || case when loan is not null then array['loan'] end
    || case when network is not null then array['network'] end
    ) as taxonomy_fields,
    array(select distinct unnest(
        service || payment || transfer || account_type || card || identification ||
        security || currency || stock_market || loan || network
    ))::text[] as taxonomy_values,
    (array[]::text[]
    || case when fraud = true then array['fraud'] end
    || case when complaint = true then array['complaint'] end
    || case when harassment = true then array['harassment'] end
    || case when access = true then array['access'] end
    || case when delay = true then array['delay'] end
    || case when interface = true then array['interface'] end
    || case when charges = true then array['charges'] end
    ) as categories
from raw_data rd
inner join processed_data pd on rd.identifier = pd.raw_data_id
where rd.is_deleted = false and emotion is not null
order by event_time desc
;

--rollback DROP VIEW processed_data_view_v1;
