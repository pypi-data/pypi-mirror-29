# Somatic Structural Variants
Information about the file/information format for somatic structural variants.

## Structure

Be aware that each of the following listings represent a **tab-separated** column field in the input SNV file. The **column names**
in the header must be specified as followed:

* [type](#type)
* [gene](#gene)
* [effect](#effect)
* [left_bp](#leftbp)
* [right_bp](#rightbp)

---

### <a name="type"></a>'type'
The copy number variation type. Currently an enumeration of [Manta](https://github.com/Illumina/manta) SVTYPE:

* DEL
* INS
* DUP
* INV
* CNV
* BND

**Example**

``type: del``

---

### <a name="gene"></a>'gene'
[HGNC](https://www.genenames.org) formatted gene name.

**Example**

``gene: tumor protein p53``

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

**Example**

``effect: activating``

---

### <a name="leftbp"></a>'left\_bp'
The estimated position of the left break point.

**Example**

``left_bp: chr1:200-300``

---

### <a name="rightbp"></a>'right\_bp'
The estimated position of the right break point.

**Example**

``right_bp: chr1:200-300``
