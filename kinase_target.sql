USE chembl;

DROP TABLE IF EXISTS target_cleaned;
CREATE TABLE target_cleaned AS (
    SELECT *
    FROM target_dictionary AS t
    WHERE target_type='SINGLE PROTEIN'
          AND organism='Homo sapiens'
);
ALTER TABLE target_cleaned ADD INDEX (tid);

# 
DROP TABLE IF EXISTS kinase_target;
CREATE TABLE kinase_target AS (
    SELECT t.gene, t.pref_name, td.tid, td.target_type, td.chembl_id
    FROM kinase_names_chembl AS t
    inner join target_cleaned as td
    on t.pref_name = td.pref_name
);
ALTER TABLE kinase_target ADD INDEX (tid);



DROP TABLE if exists target_assays;
create table target_assays as (
    select a.tid, kt.chembl_id, a.assay_id, kt.pref_name, kt.gene, kt.target_type
    from assays as a
    inner join kinase_target as kt
    on a.tid = kt.tid
);
alter table target_assays add index (assay_id);


DROP TABLE if exists assays_activities;
create table assays_activities as (
    select a.activity_id, a.assay_id, a.molregno, a.standard_value, a.standard_units, 
    a.standard_type, published_relation, ta.tid, ta.chembl_id as target_chembl_id, ta.pref_name,
    ta.gene, ta.target_type
    from activities as a
    inner join target_assays as ta 
    on a.assay_id = ta.assay_id
);
alter table assays_activities add index (activity_id);
alter table assays_activities add index (molregno);



DROP TABLE if exists compound_kinase;
create table compound_kinase as (
    select cs.canonical_smiles, a.*
    from compound_structures as cs
    inner join assays_activities as a
    on cs.molregno = a.molregno
);
alter table compound_kinase add index (target_chembl_id);

DROP table if exists kinase_chemblid;
create table kinase_chemblid as (
    select ck.*, cl.chembl_id, entity_type, entity_id, status  
    from compound_kinase as ck
    inner join chembl_id_lookup as cl
    on ck.target_chembl_id = cl.chembl_id
);




#join uniprot
alter table kinase_chemblid drop column chembl_id;
drop table if exists kinase_protein;
create table kinase_protein as (
    select ku.*, kc.*
    from kinase_chemblid as kc
    inner join kinase_uniprot as ku
    on ku.chembl_id = kc.target_chembl_id
);
alter table kinase_protein add index (chembl_id);
alter table kinase_protein add index (entry);



use chembl;
DROP table if exists kinase_activity_cleaned;
create table kinase_activity_cleaned as (
    select
    *
    from kinase_protein
      WHERE published_relation = '='
        AND standard_type IN ('IC50', 'EC50', 'Ki')
        AND standard_units = 'nM'
);
SELECT count(*) from kinase_activity_cleaned;
-- 121945





#merge activities
DROP TABLE IF EXISTS kinase_activity_merged;
CREATE TABLE kinase_activity_merged AS (
    select 
    *,
    avg(log10(standard_value)) AS mu,
    std(log10(standard_value)) AS sigma
      from kinase_protein
      GROUP BY molregno, tid, standard_type
);
# drop data points with high variance
DELETE FROM kinase_activity_merged WHERE sigma>=1;


use chembl;
DROP TABLE IF EXISTS kinase_activity_500;
CREATE TABLE kinase_activity_500 AS (
    select 
    *
      from kinase_activity_merged
      where standard_value< 500
      GROUP BY molregno, tid, standard_type

);

use chembl;
DROP table if EXISTS kinase_activity_500_indication;
create table kinase_activity_500_indication as (
    select 
    k500.*,di.drugind_id,di.max_phase_for_ind,di.mesh_id,di.mesh_heading,di.efo_id,di.efo_term
      from kinase_activity_500 as k500
      inner join drug_indication as di
      on k500.molregno = di.molregno

);

use chembl;
select count(DISTINCT tid) from kinase_activity_500;
-- 211

select count(DISTINCT molregno) from kinase_activity_500;
-- 41667

-- mddr 1489


show viriables like "%_buffer%"
-- mysql -u root -p chembl -e "select * from nerv_target" > nerv_target.txt

SET GLOBAL innodb_buffer_pool_size = 6000000000

SELECT standard_type,count(*) as Num from kinase_chemblid GROUP BY standard_type order by Num DESC;


use chembl;
drop table if exists nerv_n;
create table nerv_n as (
	select * 
	from molecule_atc_classification where level5 like 'N%');
ALTER TABLE nerv_n ADD INDEX (molregno);


drop table if exists nerv_name;
create table nerv_name as (
    select n.*, nn.who_name from nerv_n as n
    inner join atc_classification as nn
    on n.level5 = nn.level5
);
ALTER TABLE nerv_name ADD INDEX (molregno);



drop table if exists nver_structure;
create table nver_structure as (
    select n.*, s.canonical_smiles from nerv_name as n
    inner join compound_structures as s 
    on n.molregno = s.molregno
);
alter table nver_structure add index (molregno);

drop table if exists nerv_chemblid;
create table nerv_chemblid as (
    select s.*, a.chembl_id as mol_chembl_id 
    from nver_structure as s 
    inner join molecule_dictionary as a 
    on s.molregno = a.molregno
);
alter table nerv_chemblid add index (molregno);


drop table if exists nerv_indication;
create table nerv_indication as (
    select c.*, d.mesh_id, d.mesh_heading, d.efo_id, d.efo_term
    from nerv_chemblid as c 
    inner join drug_indication as d 
    on c.molregno = d.molregno
);
alter table nerv_indication add index(molregno);



-- 这里没运行完
drop table if exists nerv_activities;
create table nerv_activities as (
    select s.*, a.activity_id, a.assay_id, a.standard_value, a.standard_type, a.standard_units 
    from nerv_indication as s 
    inner join activities as a 
    on s.molregno = a.molregno
);
alter table nerv_activities add index (activity_id);


drop table if exists nerv_assays;
create table nerv_assays as (
    select ac.*, a.tid, 
    from nerv_activities as ac 
    inner join assays as a 
    on ac.assay_id = a.assay_id
);
alter table nerv_assays add index (tid);

drop table if exists nerv_target;
create table nerv_target as (
    select na.*, nt.target_type, nt.pref_name, nt.organism, nt.chembl_id as target_chembl_id
    from nerv_assays as na
    inner join target_dictionary as nt
    on na.tid = nt.tid
);
alter table nerv_target add index (tid);



