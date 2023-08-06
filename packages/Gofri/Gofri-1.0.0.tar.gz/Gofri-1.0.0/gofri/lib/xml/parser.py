import xmltodict

class XMLParser():
    def __init__(self):
        pass

    def file_to_dict(self, file_path):
        with open(file_path, "r") as xml_file:
            xml = xml_file.read()
            return xmltodict.parse(xml, process_namespaces=True, dict_constructor=dict)