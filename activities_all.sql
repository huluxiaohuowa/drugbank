USE chembl;

# clean target
DROP TABLE IF EXISTS target_all;
CREATE TABLE target_all AS (
    SELECT tid, pref_name
    FROM target_dictionary AS t
    WHERE organism='Homo sapiens'
);
ALTER TABLE target_all ADD INDEX (tid);

# clean assay
DROP TABLE IF EXISTS assay_all;
CREATE TABLE assay_all AS (
  SELECT
    assay_id,
    t.tid as tid,
    u.pref_name,
    confidence_score,
    t.assay_type
  FROM assays as t
    INNER JOIN target_all AS u ON t.tid=u.tid
);
ALTER TABLE assay_all ADD INDEX (assay_id);
ALTER TABLE assay_all ADD INDEX (tid);
ALTER TABLE assay_all ADD INDEX (confidence_score);

# clean activities
DROP TABLE IF EXISTS activity_all;
CREATE TABLE activity_all AS (
  SELECT
    activity_id,
    v.molregno as molregno,
    canonical_smiles,
    u.tid AS tid,
    standard_type,
    u.pref_name,
    standard_value,
    standard_units,
    standard_relation
  FROM activities AS t
    INNER JOIN assay_all AS u ON t.assay_id = u.assay_id
    INNER JOIN compound_structures as v on t.molregno = v.molregno
   
  WHERE data_validity_comment IS NULL
        
);
ALTER TABLE activity_all ADD INDEX (activity_id);
ALTER TABLE activity_all ADD INDEX (molregno);
ALTER TABLE activity_all ADD INDEX (tid);
ALTER TABLE activity_all ADD INDEX (standard_type);








# merge data points
DROP TABLE IF EXISTS activity_merged;
CREATE TABLE activity_merged AS (
    SELECT
      molregno,
      canonical_smiles,
      tid,
      standard_type,
      avg(log10(standard_value)) AS mu,
      std(log10(standard_value)) AS sigma
    FROM activity_cleaned
    GROUP BY molregno, tid, standard_type
);
ALTER TABLE activity_merged ADD INDEX (molregno, tid, standard_type);
ALTER TABLE activity_merged ADD INDEX (molregno);
ALTER TABLE activity_merged ADD INDEX (tid);
ALTER TABLE activity_merged ADD INDEX (standard_type);

# drop data points with high variance
DELETE FROM activity_merged WHERE sigma>=1;

# statistics
DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks AS (
  SELECT
    tid,
    standard_type,
    count(*) AS c
  FROM activity_merged AS t
  GROUP BY tid, standard_type
);
ALTER TABLE tasks ADD INDEX (tid);
ALTER TABLE tasks ADD INDEX (standard_type);

# drop task with small amount of data points
DELETE FROM activity_merged
WHERE (tid, standard_type) NOT IN (SELECT tid, standard_type FROM tasks WHERE c>=20);


# target name look up
DROP TABLE IF EXISTS task_lookup;
CREATE TABLE task_lookup AS (
    SELECT
      t.tid AS tid,
      pref_name,
      standard_type
    FROM tasks as t
      INNER JOIN target_dictionary AS u ON t.tid=u.tid
    WHERE c>=20
);
ALTER TABLE task_lookup ADD INDEX (tid, standard_type);
ALTER TABLE task_lookup ADD INDEX (tid);
ALTER TABLE task_lookup ADD INDEX (standard_type);