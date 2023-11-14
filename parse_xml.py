import re
import wikitextparser as wtp


def preprocess_text(text):
    text = re.sub('\{\{cite .*?\}\}', ' ', text)
    text = text.replace(r"TABLETOREPLACE", " ")
    text = text.replace(r"'''", " ")
    text = text.replace(r"[[", " ")
    text = text.replace(r"]]", " ")
    text = text.replace(r"{{", " ")
    text = text.replace(r"}}", " ")
    text = text.replace("<br>", " ")
    text = text.replace("&quot;", "\"")
    text = text.replace("&amp;", "&")
    text = text.replace("& amp;", "&")
    text = text.replace("nbsp;", " ")
    text = text.replace("formatnum:", "")

    # clean residual mess from xml dump that shouldn't have made its way here.
    # a lot of this mess was reintroduced from adding in the tables and infoboxes
    text = re.sub('\| ?item[0-9]?_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?col[0-9]?_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?row[0-9]?_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?style= ?.*? ', ' ', text)
    text = re.sub('\| ?bodystyle= ?.*? ', ' ', text)
    text = re.sub('\| ?frame_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?data_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?label_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?headerstyle= ?.*? ', ' ', text)
    text = re.sub('\| ?list_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?title_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?ul_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?li_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?border-style= ?.*? ', ' ', text)
    text = re.sub('\|? ?style=\".*?\"', '', text)
    text = re.sub('\|? ?rowspan=\".*?\"', '', text)
    text = re.sub('\|? ?colspan=\".*?\"', '', text)
    text = re.sub('\|? ?scope=\".*?\"', '', text)
    text = re.sub('\|? ?align=\".*?\"', '', text)
    text = re.sub('\|? ?valign=\".*?\"', '', text)
    text = re.sub('\|? ?lang=\".*?\"', '', text)
    text = re.sub('\|? ?bgcolor=\".*?\"', '', text)
    text = re.sub('\|? ?bg=\#[a-z]+', '', text)
    text = re.sub('\|? ?width=\".*?\"', '', text)
    text = re.sub('\|? ?height=[0-9]+', '', text)
    text = re.sub('\|? ?width=[0-9]+', '', text)
    text = re.sub('\|? ?rowspan=[0-9]+', '', text)
    text = re.sub('\|? ?colspan=[0-9]+', '', text)
    text = re.sub(r'[\n\t]', ' ', text)
    text = re.sub('<.*?/>', '', text)
    text = re.sub('\|? ?align=[a-z]+', '', text)
    text = re.sub('\|? ?valign=[a-z]+', '', text)
    text = re.sub('\|? ?scope=[a-z]+', '', text)
    text = re.sub('&lt;ref&gt;.*?&lt;/ref&gt;', ' ', text)
    text = re.sub('&lt;.*?&gt;', ' ', text)
    text = re.sub('File:[A-Za-z0-9 ]+\.[a-z]{3,4}(\|[0-9]+px)?', '', text)
    text = re.sub('Source: \[.*?\]', '', text)
    text = text.replace("Country flag |", "country:")
    text = text.replace("flag |", "country:")
    text = text.replace("flagicon |", "country:")
    text = text.replace("flagcountry |", "country:")
    text = text.replace("Flagu |", "country:")
    text = text.replace("display=inline", "")
    text = text.replace("display=it", "")
    text = text.replace("abbr=on", "")
    text = text.replace("disp=table", "")
    text = text.replace("sortname |", "")

    return text


dump_file = open('/Users/emily/Documents/sample.xml',"r")
markup = dump_file.read()
selector = re.compile(r'<page>(.*?)</page>', re.DOTALL)
xml_pages = re.findall(selector, markup)
dump_file.close()

"""
parsed = wtp.parse(xml_pages[1])
text = parsed.sections[13].contents
table_data_fails = 0
for table in parsed.sections[13].tables:
    table_text = ""
    try:
        table_data = table.data(span=False)
        if len(table_data[0]) <= 2 and len(table_data) > 1 and len(table_data[0]) + 2 < len(table_data[1]):
            for elem in table_data[0]:
                if elem.strip() != "":
                    table_text += elem + ", "
            table_data = table_data[1:]
        if len(table_data) == 1:
            for elem in table_data[0]:
                if elem.strip() != "":
                    table_text += elem + ", "
        table_text += ". "
        print(table_text)
    except: # working with p_tables[table_num].data sometimes throws unexplained errors
        table_data_fails+=1
        continue
    print(len(table.data(span=False)))
    print(len(table.data(span=False)[0]))
    table_data = table.data(span=False)
    for row in range(1, len(table_data)):
        for column in range(len(table_data[row])):
            if column < len(table_data[0]) and table_data[row][column] is not None and str(table_data[row][column]).strip() != "":
                if table_data[0][column] is not None:
                    table_text += table_data[0][column] + ": "
                table_text += table_data[row][column] + ', '
        table_text += ". "
    table_text = table_text.replace("''", "")
    table_text = table_text.replace("|", " | ")
    # Try to add table in appropriate place in text.
    print(table_text)
"""

for page in xml_pages:
    page_title = page.title
    parsed = wtp.parse(page)
    for sec in parsed.sections:
        section_title = sec.title
        section_content = sec.contents  # how much section content?
        if len(sec.tables) > 0:
            for table in sec.tables:
                table_title = table.caption

                table_text = ""
                try:
                    table_data = table.data(span=False)
                    if len(table_data[0]) <= 2 and len(table_data) > 1 and len(table_data[0]) + 2 < len(table_data[1]):
                        for elem in table_data[0]:
                            if elem.strip() != "":
                                table_text += elem + ", "
                        table_data = table_data[1:]
                    if len(table_data) == 1:
                        for elem in table_data[0]:
                            if elem.strip() != "":
                                table_text += elem + ", "
                    table_text += ". "
                    print(table_text)
                except: # working with p_tables[table_num].data sometimes throws unexplained errors
                    table_data_fails+=1
                    continue
                print(len(table.data(span=False)))
                print(len(table.data(span=False)[0]))
                table_data = table.data(span=False)
                for row in range(1, len(table_data)):
                    for column in range(len(table_data[row])):
                        if column < len(table_data[0]) and table_data[row][column] is not None and str(table_data[row][column]).strip() != "":
                            if table_data[0][column] is not None:
                                table_text += table_data[0][column] + ": "
                            table_text += table_data[row][column] + ', '
                    table_text += ". "
                table_text = table_text.replace("''", "")
                table_text = table_text.replace("|", " | ")
                # Try to add table in appropriate place in text.
                #print(preprocess_text(table_text))

                print(table_title)
                print(table_text)
                print(section_title)
                print(section_content)
                print(page_title)
                
                # add table_title, table_text, section_title, section_content, and page_title into csv

        print(list(sec.tables))
    #input("Press Enter to continue...")
