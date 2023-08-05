[![Build Status](https://travis-ci.org/openvax/gtfparse.svg?branch=master)](https://travis-ci.org/openvax/gtfparse) [![Coverage Status](https://coveralls.io/repos/openvax/gtfparse/badge.svg?branch=master&service=github)](https://coveralls.io/github/openvax/gtfparse?branch=master)

gtfparse
========
Parsing tools for GTF (gene transfer format) files.

# Example usage

## Parsing all rows of a GTF file into a Pandas DataFrame

```python
from gtfparse import read_gtf_as_dataframe

# returns GTF with essential columns such as "feature", "seqname", "start", "end"
# alongside the names of any optional keys which appeared in the attribute column
df = read_gtf_as_dataframe("gene_annotations.gtf")

# filter DataFrame to gene entries on chrY
df_genes = df[df["feature"] == "gene"]
df_genes_chrY = df_genes[df_genes["seqname"] == "Y"]
```


## Getting gene FPKM values from a StringTie GTF file

```python
from gtfparse import read_gtf_as_dict

gtf_dict = read_gtf_as_dict(
    "stringtie-output.gtf",
    column_converters={"FPKM": float})

gene_fpkms = {
    gene_name: fpkm
    for (gene_name, fpkm, feature)
    in zip(gtf_dict["gene_name"], gtf_dict["FPKM"], gtf_dict["feature"])
    if feature == "gene"
}
```


