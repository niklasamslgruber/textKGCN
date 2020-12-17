import lxml.html as lh
import pandas as pd
import requests
from helper import file_utils as file


# This file downloads a list of all available WikiData relations (properties) and filters them
# The filters are:
#   * Relation categories which do not refer to a WikiData item
#   * Relations with too less data (everything below the median)
#
# The script produces two files:
#   * /all_wiki_relations.csv: Includes all relations with their type, count, category, etc.
#   * /filtered_wiki_relations.csv: Includes the relation Ids of all relations which passed the filter


def download_all_properties():
    url = "https://www.wikidata.org/wiki/Wikidata:Database_reports/List_of_properties/all"
    request = requests.get(url)

    # Get data between the <tr>..</tr> HTML tags
    doc = lh.fromstring(request.content)
    tr_elements = doc.xpath('//tr')

    columns = []
    i = 0
    # Get table headers
    for t in tr_elements[0]:
        i += 1
        header = t.text_content().rstrip("\n")
        columns.append((header, []))

    # Get table rows
    for j in range(1, len(tr_elements)):
        row = tr_elements[j]
        current_column = 0

        # Iterate through each element of the row
        for t in row.iterchildren():
            data = t.text_content()
            # Check if row is empty
            if current_column == 5:
                # Convert any numerical value to integers
                try:
                    data = data.replace(',', '')
                    data = int(data)
                except:
                    pass
            # Append the data to the empty list of the i'th column
            columns[current_column][1].append(data)
            current_column += 1

    data_dict = {title: column for (title, column) in columns}
    data_df = pd.DataFrame(data_dict)

    file.save_all_relations(data_df)


def get_all_properties(threshold=1000):
    # Last downloaded on 17.12.2020 at 12:20
    # download_all_properties()

    relations_df = file.get_all_relations()
    initial_size = relations_df.shape[0]

    # Drop all properties which are unneccessary such as URL, Math, Location data, etc.
    important_types = relations_df[~relations_df["type"].isin(["WikibaseItem"])].index
    relations_df.drop(important_types, inplace=True)

    # Filter out all relations with a count below the threshold (see statistics by using describe())
    # Currently the median (50%) is used (value: 1000)
    too_small = relations_df[relations_df["count"] < threshold].index
    relations_df.drop(too_small, inplace=True)

    # Filter out relations from manual removement
    # wrong_relations = ["P31", "P461", "P527", "P460", "P1889", "P180", "P2670", "P1269", "P1382", "P21", "P462", "P509"] # version: manual
    # wrong_relations = ["P31", "P279", "P361", "P461", "P527", "P1889", "P460", "P366", "P921", "P180", "P1269", "P1535", "P1552", "P3095", "P425"] # version: no_populars
    wrong_relations = ["P31", "P279", "P361", "P461", "P527", "P1889", "P460", "P366", "P921", "P180", "P1269", "P1535", "P1552", "P3095", "P425", "P155", "P156"] # version: filtered

    irrelevant = relations_df[relations_df["ID"].isin(wrong_relations)].index
    relations_df.drop(irrelevant, inplace=True)

    # Save to CSV ordered by count with details and without
    relations_df.sort_values(by=["count"], ascending=False, inplace=True)
    file.save_filtered_relations(relations_df["ID"])

    print(f"{initial_size - relations_df.shape[0]} items filtered out...")
    print(f"Relevant relations: {relations_df.shape[0]}")


if __name__ == '__main__':
    get_all_properties(threshold=1000)
