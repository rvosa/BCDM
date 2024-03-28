# Barcode Core Data Model
<br>

Welcome to the repository for the Barcode Core Data Model, a metadata standard designed to revolutionize the way DNA barcode data is structured, shared, and utilized across the scientific community. This standard represents a collaborative effort to establish a comprehensive framework that not only enhances data exchange but also fosters innovation in the development of tools and applications centered around DNA-based biodiversity data.

## Purpose

The purpose of the DNA Barcode Metadata Standard is to ensure that DNA barcode datasets are structured in a unified, consistent, and clear manner, facilitating interoperability and effective data sharing between research groups and databases. This standardization is intended to streamline the cataloging and analysis of biodiversity data, enabling researchers to collaborate more efficiently.

## Core Features

- Comprehensive coverage of essential data elements related to DNA based species identification, including specimen collection, DNA sequences, and taxonomic classification.

- Establishment of a common vocabulary for data interpretation

- Alignment with existing biodiversity data models and databases, including the Barcode of Life Data System (BOLD) and Darwin Core Data, streamlining data exchange.

- Serves as a foundation for the development of analytical tools, databases, and resources that utilize DNA barcode data, opening new avenues for research, conservation, and education.



1. **field_definitions.tsv**: This document provides the definitions and format for the current supported universal fields included in the Barcode Core Data Model (BCDM). 
<br>
Please notice that the BCDM field `identifier_email` is not part of the exported fields.
<br>


  
  |**Column name** | **Definition**|
  | :----------|:---------|
  |field| Standardized/universal name for the data field.|
  |data_type|  Data type of the field. For example: integer, float,string, and string:date|
  |data_format| Additional formatting constraint for the data value. For example: a timestamp field may follow this format `%d-%b-%y`; default indicates no extra formatting constraint specified. | 
  |definition | Meaning of the term, including their controlled vocabulary when applicable. |
  | |
<br>
<br>

2. **mapping_BCDM_to_BOLD.tsv**: This document provides mapping of the BCDM data fields to the BOLD Relational Database. 

<br>



  |**Column name** | **Definition**|
  | :----------|:---------|
  |bcdm_field| Standardized/universal name for the data field.|
  |bold_db | The relational database to which the data of the universal field are residing, in the format: `server`:`database_name`.  Example: db1:newdb12 |
  |bold_db_table| The specific database table to which the universal field is mapped to.|
  |bold_db_field| The specific database field to which the universal field is mapped to.|
  |rules| Set of regex used for basic data validation.
  | |
<br>
<br>

  3. **mapping_BCDM_to_BOLDrelational.tsv**: In order to provide a more convenient and streamlined access to the data, a single relational database view (aka. single pane view) containing all the universal data fields that has been defined. 
  
<br>

 

  |**Column name** | **Definition**|
  | :----------|:---------|
  |bcdm_field| Standardized/universal name for the data field.|
  |bold_field | Contains information on how to map the universal field to the database through the single pane view. Most cases the format will be the fieldname as in the single pane view. However there might be additional joins to other tables required which will be denoted with double underscore `__`.  |
  | |
<br>
<br>

  4. **mapping_BCDM_to_DWC.tsv**: This document provides the mapping of the BCDM to Darwin Core standard. Please notice that not all BCMD fields have an equivalent term in the Darwin Core standard and therefore they will not be part of the export. DarwinCore fields can be found in the following link: `[Darwin Reference Guide] (https://dwc.tdwg.org/terms/)`
 
<br>


  
  |**Column name** | **Definition**|
  | :----------|:---------|
  |bcdm_field | Standardized/universal name for the data field.|
  |dwc_field | Corresponding term in the Darwin Core glossary.|
  |bcdm_type|Data type of the field as in the BCDM. For example: integer, float,string, and string:date |
  |bcdm_format| Additional formatting constraint for the data value as in the BCDM. For example: a timestamp field may follow this format `%d-%b-%y`; default indicates no extra formatting constraint specified.  |
  |dwc_type|Data type of the field as in the Darwin Core standard.|
  |dwc_format| Additional formatting constraint for the data value as in the Darwin Core standard.|
  | |
