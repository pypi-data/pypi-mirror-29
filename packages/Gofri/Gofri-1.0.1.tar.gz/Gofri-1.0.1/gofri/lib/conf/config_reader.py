from gofri.lib.xml.parser import XMLParser


class ConfigReader:
    def __init__(self, root_path):
        self.root_path = root_path
        self.conf_xml_path = self.root_path + "/conf.xml"
        self.secret_conf_xml = self.root_path + "/secret-conf.xml"
        self.app_conf_xml = self.root_path + "/app-conf.xml"

    def get_conf_xml(self, conf_xml_path=None):
        if conf_xml_path is None:
            conf_xml_path = self.conf_xml_path
        xmlparser = XMLParser()
        return xmlparser.file_to_dict(conf_xml_path)

    def get_dict_config(self, d, *keys):
        result = dict(d)
        for key in keys:
            try:
                if result[key] is None:
                    return None
            except KeyError:
                return None
            result = result[key]
        return result

