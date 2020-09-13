from os.path import isfile
import requests
import lxml.html as lh
import pandas as pd
from utils import get_kg_data_path

all_relations_path = f"{get_kg_data_path()}/data/all_wiki_relations.csv"
filtered_detail_relations_path = f"{get_kg_data_path()}/data/filtered_wiki_relations_detail.csv"
filtered_relations_path = f"{get_kg_data_path()}/data/filtered_wiki_relations.csv"


def download_all_properties():
    url = "https://www.wikidata.org/wiki/Wikidata:Database_reports/List_of_properties/all"
    request = requests.get(url)
    # Save page content
    doc = lh.fromstring(request.content)
    # Get data between the <tr>..</tr> HTML tags
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
    write_csv(data_df, all_relations_path)


def get_all_properties(threshold=1000):
    if not isfile(all_relations_path):
        download_all_properties()

    relations_df = read_csv(all_relations_path)
    initial_size = relations_df.shape[0]

    # Drop all properties which are unneccessary such as URL, Math, Location data, etc.
    important_types = relations_df[~relations_df["Data type"].isin(["WikibaseItem", "String", "Monolingualtext"])].index
    relations_df.drop(important_types, inplace=True)

    # Filter out all relations with a count below the threshold (see statistics by using describe())
    # Currently the median (50%) is used (value: 1000)
    too_small = relations_df[relations_df["Count"] < threshold].index
    relations_df.drop(too_small, inplace=True)

    # Save to CSV ordered by count with details and without
    relations_df.sort_values(by=["Count"], ascending=False, inplace=True)
    write_csv(relations_df, filtered_detail_relations_path)
    write_csv(relations_df["ID"], filtered_relations_path)
    print(f"{initial_size - relations_df.shape[0]} items filtered out...")


def read_csv(path):
    return pd.read_csv(path, index_col=None, sep="+")


def write_csv(dataframe, path):
    dataframe.to_csv(path, index=False, sep="+")


if __name__ == '__main__':
    get_all_properties(threshold=1000)
