import xml.etree.ElementTree as ET

class Path:
    def __init__(self, xml_dict):
        print(xml_dict)
        self.source = xml_dict['source']
        self.dest = xml_dict['dest']
        self.maxLatency = xml_dict['maxLatency']
        self.path = xml_dict['path']
    
    def show(self):
        print('\n   Path:', end = ' ')
        print(f'source: {self.source}', end = ' ')
        print(f'dest: {self.dest}', end = ' ')
        print(f'maxLatency: {self.maxLatency}', end = ' ')
        print(f'path: {self.path}', end = ' ')

class NetElement:
    def __init__(self, xml_dict):
        self.name = xml_dict['name']
        self.number = xml_dict['number']
        self.ports = xml_dict['ports']
        self.delay = xml_dict['delay']
        self.x = xml_dict['x']
        self.y = xml_dict['y']

    def ne_show(self):
        print(f'name:{self.name}', end=' ')
        print(f'number:{self.number}', end=' ')
        print(f'ports:{self.ports}', end=' ')
        print(f'delay:{self.delay}', end=' ')
        print(f'x:{self.x}', end=' ')
        print(f'y:{self.y}', end=' ')

class EndSystem(NetElement):
    def show(self):
        print('\nEndSystem:', end=' ')
        self.ne_show()

class Switch(NetElement):
    def show(self):
        print('\nSwitch:', end=' ')
        self.ne_show()

class Partition:
    def __init__(self, xml_dict):
        self.connectedTo = xml_dict['connectedTo']
        self.name = xml_dict['name']
        self.number = xml_dict['number']
        self.x = xml_dict['x']
        self.y = xml_dict['y']

    def show(self):
        print('\nPartition:', end=' ')
        print(f'connectedTo:{self.connectedTo}', end=' ')
        print(f'name:{self.name}', end=' ')
        print(f'number:{self.number}', end=' ')
        print(f'x:{self.x}', end=' ')
        print(f'y:{self.y}', end=' ')

class Link:
    def __init__(self, xml_dict):
        self.capacity = xml_dict['capacity']
        self.fromType = xml_dict['fromType']
        self.to = xml_dict['to']
        self.toType = xml_dict['toType']
    
    def show(self):
        print('\nLink:', end=' ')
        print(f'capacity:{self.capacity}', end=' ')
        print(f'fromType:{self.fromType}', end=' ')
        print(f'to:{self.to}', end=' ')
        print(f'toType:{self.toType}', end=' ')

class VirtualLink(Path):
    def __init__(self, xml_dict, paths_list):
        self.bag = xml_dict['bag']
        self.dest = xml_dict['dest'] # TODO: revisit this
        self.id = xml_dict['id']
        self.name = xml_dict['name']
        self.lmax = xml_dict['lmax']
        self.number = xml_dict['number']
        self.source = xml_dict['source']
        self.route = [Path(path_dict) for path_dict in paths_list]

    def show(self):
        print("\nVirtualLink:", end = ' ')
        print(f'bag:{self.bag}', end = ' ')
        print(f'dest:{self.dest}', end = ' ')
        print(f'id:{self.id}', end = ' ')
        print(f'name:{self.name}', end = ' ')
        print(f'lmax:{self.lmax}', end = ' ')
        print(f'number:{self.number}', end = ' ')
        print(f'source:{self.source}', end = ' ')
        for path in self.route:
            path.show()
            
class AFDX_network:
    resources = {}
    virtualLinks = []
    dataFlows = []

    def __init__(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for child in root:
                if child.tag == 'virtualLinks':
                    for child_inside in child:
                        new_vl_paths = []
                        for child_i_i in child_inside:
                            new_vl_paths.append(child_i_i.attrib)
                        self.virtualLinks.append(VirtualLink(child_inside.attrib, new_vl_paths))
                if child.tag == 'resources':
                    for child_inside in child:
                        match child_inside.tag:
                            case 'endSystem':
                                resource_obj = EndSystem(child_inside.attrib)
                            case 'switch':
                                resource_obj = Switch(child_inside.attrib)
                            case 'partition':
                                resource_obj = Partition(child_inside.attrib)
                            case 'link':
                                resource_obj = Link(child_inside.attrib)
                            
                        if child_inside.tag in self.resources:
                            self.resources[child_inside.tag].append(resource_obj)
                        else:
                            self.resources[child_inside.tag] = [resource_obj]
    def show(self):
        for _, element_list in self.resources.items(): 
            for element in element_list:
                element.show()
        for vl in self.virtualLinks:
            vl.show()
        print('\n')

