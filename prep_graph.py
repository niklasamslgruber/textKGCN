from analyze_properties import get_all_properties
from match_kg_data import create_wiki_mappings
from create_kg_edges import create_doc2doc_edges


def setup():
    print("\n\n[WARNING]: This process requires an active internet connection and may take a while\n\n")
    # Load all WikiData properties and filter them
    get_all_properties()
    print("Successfully downloaded and filtered all WikiData relations")

    # Map words from dataset to WikiData entities
    create_wiki_mappings()
    print("Successfully mapped vocabulary to WikiData entities and relations")

    # Build doc2doc edges based on WikiData graph
    create_doc2doc_edges()
    print("Successfully created all doc2doc edges")

    print("\nYou're now ready to run textKGCN!")


if __name__ == '__main__':
    setup()