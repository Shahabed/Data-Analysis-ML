

# Description:

There are various challenges in the processing of the FAERS database, which create a necessity for the data pre/processing.
These challenges can be summarized as follow:


**1.** The main challenge is the hierarchical structure of the database. Different aspects of data are stored separately in a set of subgroups. These subgroups are relatedhierarchically by a key called primary_id. The function ADR_data_connector is design to tackle the above challenge. This function is stored in function_set and calledlater in the processing algorithm.


**2.** There are some corruptions in the structure of dataframes, containing the FAERS database, which is addressed in this algorithm.


**3.** Also, we would like to find out the number of unique drug names and reaction terms.
This information will help the future analyses and increase our confidence on the sufficiency of data for the further processes.
