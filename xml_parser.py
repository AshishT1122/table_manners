import re
import wikitextparser as wtp
import unidecode
import csv


def preprocess_text(text):
    """
    Cleans the given text by removing or replacing unnecessary characters and patterns.
    """
    # List of regex patterns and their replacements
    patterns = [
        (r'\{\{cite .*?\}\}', ' '),  # Remove citations
        (r"TABLETOREPLACE|'''|\[\[|\]\]|\{\{|\}\|<br>|&quot;|& amp;|nbsp;|formatnum:", ' '),
        (r'&amp;', '&'),
        # Removing various style and layout elements from the XML
        (r'\| ?\w*?style= ?.*? ', ' '),
        (r'\|?\s?style=\".*?\"', ' '),
        (r'\|?\s?(rowspan|colspan|scope|align|valign|lang|bgcolor|bg|width|height)=\".*?\"', ' '),
        (r'\|?\s?(rowspan|colspan|width|height)=[0-9]+', ' '),
        (r'\|?\s?(align|valign|scope)=[a-z]+', ' '),
        # Removing other specific patterns
        (r'[\n\t]', ' '),
        (r'<.*?/>', ''),
        (r'&lt;ref&gt;.*?&lt;/ref&gt;', ' '),
        (r'&lt;.*?&gt;', ' '),
        (r'File:[A-Za-z0-9 ]+\.[a-z]{3,4}(\|[0-9]+px)?', ''),
        (r'Source: \[.*?\]', ''),
    ]

    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)

    # Additional replacements for flags and other specific patterns
    flag_replacements = ["Country flag |", "flag |", "flagicon |", "flagcountry |", "Flagu |"]
    for flag in flag_replacements:
        text = text.replace(flag, "country:")

    additional_replacements = {
        "display=inline": "",
        "display=it": "",
        "abbr=on": "",
        "disp=table": "",
        "sortname |": "",
        "\"": " ",
        "&": " ",
    }

    for old, new in additional_replacements.items():
        text = text.replace(old, new)

    return text


def read_xml_pages(xml_file_path):
    """
    Reads XML file and extracts pages.
    """
    with open(xml_file_path, "r") as dump_file:
        markup = dump_file.read()

    selector = re.compile(r'<page>(.*?)</page>', re.DOTALL)
    return re.findall(selector, markup)

def process_page(page):
    """
    Processes a single page from the XML dump.
    """
    page_title = unidecode.unidecode(re.search('<title>(.*?)</title>', page).group(1).strip())
    parsed = wtp.parse(page)

    page_data = []

    for sec in parsed.sections:
        section_title = sec.title
        section_content = sec.contents  # To be processed later
        if sec.tables:
            for table in sec.tables:
                table_data = process_table(table)
                if table_data:
                    page_data.append([table_data, section_title, section_content, page_title])

    return page_data

def process_table(table):
    """
    Processes a single table within a page.
    Returns the table title and the processed table content.
    """
    # Initialize variables
    table_text = ""
    table_title = table.caption or "No Title"

    try:
        # Extract table data
        table_data = table.data(span=False)

        # Handle special cases for table data structure
        if len(table_data) > 1:
            header_row = table_data[0]
            data_rows = table_data[1:]

            for row in data_rows:
                for column, value in enumerate(row):
                    if column < len(header_row) and value and value.strip():
                        header = header_row[column] or "Column"
                        table_text += f"{header}: {value.strip()}, "
                table_text += ". "  # End of row marker

        elif len(table_data) == 1:
            # Single row table
            for value in table_data[0]:
                if value and value.strip():
                    table_text += f"{value.strip()}, "
            table_text += ". "

    except Exception as e:
        print(f"Error processing table: {e}")
        return None

    # Clean up the table title and text
    clean_table_title = preprocess_text(table_title)
    clean_table_text = preprocess_text(table_text)

    return clean_table_title, clean_table_text

def write_to_csv(data, csv_file_path):
    """
    Writes processed data to a CSV file.
    """
    with open(csv_file_path, "w", newline='') as file:
        writer = csv.writer(file)
        col_headers = ['table_title', 'table_content', 'section_title', 'section_content', 'page_title']
        writer.writerow(col_headers)
        for row in data:
            writer.writerow(row)

def main():
    """
    Main function to process the XML dump and write to a CSV file.
    """
    # Constants for file paths
    XML_FILE_PATH = '/Users/emily/Documents/sample.xml'
    CSV_FILE_PATH = 'table_data_test.csv'
    xml_pages = read_xml_pages(XML_FILE_PATH)
    all_data = []

    for page in xml_pages:
        page_data = process_page(page)
        all_data.extend(page_data)

    write_to_csv(all_data, CSV_FILE_PATH)

if __name__ == "__main__":
    main()
