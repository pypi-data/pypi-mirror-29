# Metadata
Information about the file/information format for metadata.

## Structure

Be aware that each of the following listings represent a **tab-separated** column field in the input SNV file. The **column names**
in the header must be specified as followed:

* [diagnosis](#diagnosis)
* [tumor_content](#tumorcontent)
* [pathogenic_germline](#pathogenicgermline)
* [mutational_load](#load)
* [chromosomal_instability](#instability)
* [quality_flags](#flags)
* [reference_genome](#ref)

---

### <a name="diagnosis"></a>'diagnosis'
A size description of the diagnosis. Either in ICD10 or HPO terms.

**Example**

``diagnosis: C79.6 Sekundäre bösartige Neubildung des Ovars``

---

### <a name="tumorcontent"></a>'tumor\_content'
The tumor content as ``float`` type of the sequenced sample, determined by a pathologist. 

**Example**

``tumor_content: 0.5``

---

### <a name="pathogenicgermline"></a>'pathogenic\_germline'
Boolean information about the pathogenity of the germline. Values will be one of:

* yes
* no
* NA

**Example**

``pathogenic_germline: yes``

---

### <a name="load"></a>'mutational\_load'
Categorial information about the mutational load. Currently an enumeration of:

* low
* medium
* high

**Example**

``mutational_load: low``

---

### <a name="instability"></a>'chromosomal\_instability'
Boolean information about the chromosomal instablity. Currently an enumeration of:

* yes
* no

**Example**

``chromosomal_instability: yes``

---

### <a name="flags"></a>'quality\_flags'
Semicolon-separated list of quality flags for the SNVs, CNVs, SVs and DNA amount.

**Example**

``quality_flags: low_quality_snvs;high_quality_cnvs``

---

### <a name="ref"></a>'reference\_genome'
The reference genome used for the analysis.

**Example**

``reference_genome: hg19``