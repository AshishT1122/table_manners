import re
import csv
import unidecode
import wikitextparser as wtp

# Constants for file paths
XML_FILE_PATH = 'sample.xml'
TSV_FILE_PATH = 'linearized_table_data.tsv'


def preprocess_text(text):
    """Cleans up the input text by removing or replacing unwanted patterns."""
    if text is None:
        return ""

    def remove_patterns(patterns, replacement):
        """Applies multiple regex substitutions with the same replacement."""
        nonlocal text
        for pattern in patterns:
            text = re.sub(pattern, replacement, text)

    # Combine similar regex patterns
    citation_patterns = [r'\{\{cite .*?\}\}', r'\{\{Citation needed.*?\}\}', r'\{\{sfn.*?\}\}']
    style_patterns = [
        r'\| ?(item|col|row|bodystyle|frame_?style|data_?style|label_?style|headerstyle|list_?style|title_?style|ul_?style|li_?style|border-style)= ?.*? ',
        r'\|? ?style=\".*?\"', r'\|? ?(rowspan|colspan|scope|align|valign|lang|bgcolor|bg|width|height)=\".*?\"',
        r'\|? ?(width|height|rowspan|colspan)=[0-9]+', r'\|? ?(align|valign|scope)=[a-z]+'
    ]
    html_patterns = [r'<.*?/>', r'&lt;ref&gt;.*?&lt;/ref&gt;', r'&lt;.*?&gt;']
    simple_replacements = [
        ("{{break}}", " "), ("{{clear}}", ""), ("TABLETOREPLACE", " "), ("'''", " "),
        ("[[", " "), ("]]", " "), ("{{", " "), ("}}", " "), ("( )", " "), ("<br>", " "),
        ("&quot;", "\""), ("&amp;", "&"), ("& amp;", "&"), ("nbsp;", " "),
        ("formatnum:", ""), ("bartable", ""), ("Country flag |", "country:"),
        ("flag |", "country:"), ("flagicon |", "country:"), ("flagcountry |", "country:"),
        ("Flagu |", "country:"), ("display=inline", ""), ("display=it", ""),
        ("abbr=on", ""), ("disp=table", ""), ("sortname |", "")
    ]

    # Apply combined regex patterns
    remove_patterns(citation_patterns, ' ')
    remove_patterns(style_patterns, ' ')
    remove_patterns(html_patterns, ' ')
    text = re.sub(r'[\n\t]', ' ', text)
    text = re.sub('File:[A-Za-z0-9 ]+\.[a-z]{3,4}(\|[0-9]+px)?', '', text)
    text = re.sub('Source: \[.*?\]', '', text)
    text = re.sub("\|\s*lc=y", "", text)
    text = re.sub("\s+", " ", text)

    # Apply simple string replacements
    for old, new in simple_replacements:
        text = text.replace(old, new)

    return text


def read_xml_pages(file_path):
    """Reads the XML pages from the given file path."""
    with open(file_path, "r", encoding='utf-8') as file:
        content = file.read()

    # Extract pages using regex
    page_selector = re.compile(r'<page>(.*?)</page>', re.DOTALL)
    return re.findall(page_selector, content)

def process_tables(xml_pages):
    """Processes tables in each XML page and writes them to TSV."""
    col_headers = ['pid', 'article_title', 'text']
    pid = 0
    table_data_fails = 0

    with open(TSV_FILE_PATH, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(col_headers)

        for page in xml_pages:
            page_title = unidecode.unidecode(re.search('<title>(.*?)</title>', page).group(1).strip())
            parsed = wtp.parse(page)

            for section in parsed.sections:
                num_tables = process_section(section, page_title, writer, pid, table_data_fails)
                pid += int(num_tables or 0)

def process_section(section, page_title, writer, pid, table_data_fails):
    """Processes a single section from a Wikipedia page."""
    section_title = preprocess_text(section.title)
    num_tables = 0
    if not section.tables:
        return

    section_content = " " + section.contents.replace("\n", " ") + " "
    context_split = re.split(r"\{\|\s*class=&quot;.*?wikitable.*?\|\}", section_content)

    for i, table in enumerate(section.tables):
        table_title = "" if table.caption is None else preprocess_text(table.caption.strip())
        preceding_content, proceeding_content = extract_context(context_split, i)

        table_text = extract_table_text(table)

        if table_text:
            linearized_table_context = build_linearized_context(
                page_title, section_title, preceding_content, table_title, table_text, proceeding_content
            )
            writer.writerow([pid + num_tables, page_title, linearized_table_context])
            num_tables += 1
        else:
            table_data_fails += 1
    return num_tables

def extract_context(context_split, index):
    """Extracts preceding and proceeding context for a table."""
    context_before = preprocess_text(context_split[index]).strip()
    context_after = preprocess_text(context_split[index + 1]).strip()
    return context_before, context_after

def extract_table_text(table):
    """Extracts and formats text from a table."""
    table_text = ""
    try:
        table_data = table.data(span=False)
        # Add more logic here if needed
    except Exception as e:
        print(f"Error processing table data: {e}")
        return ""

    # Process each row and column
    for row in table_data[1:]:  # Skip header row
        for column, cell in enumerate(row):
            if cell and cell.strip():
                column_title = table_data[0][column].strip() if table_data[0][column] else "Category"
                table_text += f"{column_title}: {cell}, "
        table_text += ". "

    return preprocess_text(table_text).strip()

def build_linearized_context(page_title, section_title, preceding_content, table_title, table_text, proceeding_content):
    """Builds a linearized context string for a table."""
    return f"{page_title} ; {section_title} ; {preceding_content} ; {table_title} ; {table_text} ; {proceeding_content}"

# Main execution
xml_pages = read_xml_pages(XML_FILE_PATH)
process_tables(xml_pages)
