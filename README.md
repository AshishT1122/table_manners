# **Table Manners**: Improving Digestion of Tabular Data via Contextualization and Handling of Non-Uniform Tables

| Title    | **Table Manners**: Improving Digestion of Tabular Data via Contextualization and Handling of Non-Uniform Tables   |
|-----------|----------------|
| Authors  | Ashish Thakur & Emily Okabe|
| Mentor   | Heidi Zhang         |

## Overview
"Table Manners" is a research project focusing on enhancing the processing and contextualization of tabular data in Open-Domain Question Answering (ODQA) systems. Our work builds upon existing methods, introducing improved techniques for linearizing and integrating table data into the Wikipedia corpus for more effective information retrieval.

## Installation
To set up the environment for this project, follow these steps:
1. Ensure Python 3.9 or higher is installed.
2. Install required Python packages:
   ```
   pip install wikitextparser unidecode
   ```

## Data Preparation
1. Download the Wikipedia XML Dump from [here](https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2) and uncompress it (note: the uncompressed file is >90GB).
2. Set the `XML_FILE_PATH` variable in `parse_xml` script to the path of the uncompressed Wiki XML dump.
3. Run `python parse_xml` to generate `linearized_table_data.tsv`, containing the contextualized, linearized table data.

## Using ColBERTv2 with Google Colab
For optimal performance, we recommend using Google Colab with the following setup:
1. Upload the `table_manners_ColBERTv2.ipynb` file to Google Colab.
2. Connect to a runtime with at least a T4 GPU (more capable GPU recommended).
3. Ensure the selected GPU is enabled under the "Hardware Accelerator" tab.
4. Add `linearized_table_data.tsv` to your Colab workspace at `/content/linearized_table_data.tsv`.

## Research Workflow
The `table_manners_ColBERTv2.ipynb` notebook, a modification of the [original ColBERTv2 notebook](https://colab.research.google.com/github/stanford-futuredata/ColBERT/blob/main/docs/intro2new.ipynb), guides you through:
- Downloading the `wiki-all-8-4-tamber` variant of the `castorini/odqa-wiki-corpora` dataset.
- Indexing the original and modified datasets using ColBERTv2.
- Querying both datasets with CompMix dataset questions related to table data.
- Evaluating retrieval accuracy among the top-1, top-5, and top-10 retrieved passages.

## Authors and Acknowledgments
- **Authors**: Ashish Thakur & Emily Okabe
- **Mentor**: Heidi Zhang

## Note
This project is part of ongoing research and development in the field of ODQA. Contributions, suggestions, and discussions are welcome to further enhance the capabilities of these systems in handling diverse data formats, especially non-uniform and complex table structures. 

---

For detailed instructions, refer to the comments and annotations within the `table_manners_ColBERTv2.ipynb` notebook. The repository also includes scripts and data files essential for replicating our research and experimenting with further improvements. 

Feel free to raise issues or contribute to this project as we collectively push the boundaries of knowledge retrieval and question answering technologies.
