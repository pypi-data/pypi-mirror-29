# Copy Number Variations (CNVs)
Information about the file/information format for somatic/germline CNVs.

## Structure

Be aware that each of the following listings represent a **tab-separated** column field in the input SNV file. The **column names**
in the header must be specified as followed:

* [size](#size)
* [type](#type)
* [copy_number](#copynumber)
* [gene](#gene)
* [exons](#exons)
* [transcript](#transcript)
* [chr](#chr)
* [start](#start)
* [end](#end)
* [effect](#effect)

---

### <a name="size"></a>'size'
A size description of the copy number variation. Currently an enumeration of:

* chromosome
* p-arm
* q-arm
* partial p-arm
* partial q-arm
* focal
* non-focal
* cluster

**Example**

``size: q-arm``

---

### <a name="type"></a>'type'
The copy number variation type. Currently an enumeration of:

* del
* dup
* amp
* loh
* ins

**Example**

``type: del``

---

### <a name="copynumber"></a>'copy\_number'
The copy number of the variation.

**Example**


``copy_number: 1``

---

### <a name="gene"></a>'gene'
[HGNC](https://www.genenames.org) formatted gene name.

**Example**

``gene: tumor protein p53``

---

### <a name="exons"></a>'exons'
Information about the affected exons of a gene.

**Example**

``exons: whole gene``

---

### <a name="transcript"></a>'transcript'
Transcript reference identifier. Refseq or Ensembl.

**Example**

``transcript: NM_001143990.1``

---

### <a name="chr"></a>'chr'
The chromosome location of the variant.

**Example**

``chr: chr1``

---

### <a name="start"></a>'start'
The genomic start position of the variant.

**Example**

``start: 12500``

---

### <a name="end"></a>'end'
The genomic end position of the variant.

**Example**

``end: 13000``

---

### <a name="effect"></a>'effect'
The predicted or annotated effect of the variant. Currently an enumeration of:

Somatic CNVs:

* activating
* inactivating
* function_changed
* probably\_activating
* probably\_inactivating
* probably\_function\_change
* ambigious
* benign
* NA

Germline CNVs ([ACMG](https://www.acmg.net/)):

* pathogenic
* probably_pathogenic

**Example**

``effect: activating``

