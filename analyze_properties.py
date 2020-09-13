import requests
import lxml.html as lh
import pandas as pd
from utils import get_kg_data_path


def load_all_properties():
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
                    print(f"Fail for {i}")
                    pass
            # Append the data to the empty list of the i'th column
            columns[current_column][1].append(data)
            current_column += 1

    data_dict = {title: column for (title, column) in columns}
    data_df = pd.DataFrame(data_dict)
    data_df.to_csv(f"{get_kg_data_path()}/data/all_wiki_relations.csv", index=False, sep="+")


if __name__ == '__main__':
    load_all_properties()
