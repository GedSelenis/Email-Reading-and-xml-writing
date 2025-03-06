import xml.etree.cElementTree as ET

# Classes
class Truck:
    def __init__(self,name_plate,load_capacity,weight):
        self.name_plate = name_plate
        self.load_capacity = load_capacity
        self.weight = weight

class Pallet:
    def __init__(self,goods,BIN,weight):
        self.goods = goods
        self.BIN = BIN
        self.weight = weight

# Public variables
DataFileName = "Trucking info.msg"
XMLFileName = "TruckData.xml"
AllLines = []
TruckInfo = Truck("","","")
AllPallets = []


# Reads whole email file
def ReadAllFile(file_name):
    file = open(file_name, "r", encoding="utf8", errors="ignore")
    AllLines.extend(file.readlines())
    file.close()

# Reads data from email file
def ReadDataFromFile():
    reading_truck = False
    reading_pallet = False
    line: str

    pallet_goods = ""
    pallet_BIN = []
    pallet_weight = ""

    for line in AllLines:
        if reading_truck:
            if line.__contains__("Pallet info:"):
                reading_pallet = True
                reading_truck = False
            elif line.__contains__("NamePlate:"):
                TruckInfo.name_plate = ExtractData(line,"NamePlate:")
            elif line.__contains__("LoadCapacity:"):
                TruckInfo.load_capacity = ExtractData(line,"LoadCapacity:")
            elif line.__contains__("Weight:"):
                TruckInfo.weight = ExtractData(line,"Weight:")
        elif reading_pallet:
            if line.__contains__("Truck info:") or line.__contains__("</body>"):
                reading_pallet = False
                reading_truck = True
                for bin in pallet_BIN:
                    new_pallet = Pallet(pallet_goods,bin,pallet_weight)
                    AllPallets.append(new_pallet)
            elif line.__contains__("Pallet info:"):
                for bin in pallet_BIN:
                    new_pallet = Pallet(pallet_goods,bin,pallet_weight)
                    AllPallets.append(new_pallet)
                pallet_goods = ""
                pallet_BIN = []
                pallet_weight = ""
            elif line.__contains__("Goods:"):
                pallet_goods = ExtractData(line,"Goods:")
            elif line.__contains__("BIN:"):
                pallet_BIN.extend(ExtractBIN(ExtractData(line,"BIN:")))
            elif line.__contains__("Weight:"):
                pallet_weight = ExtractData(line,"Weight:")
        elif line.__contains__("Truck info:"):
            reading_truck = True
        elif line.__contains__("Pallet info:"):
            reading_pallet = True

# Extracts specific data from the line
def ExtractData(line: str, data_type: str):
    info = ""
    line = line.replace(data_type,"")
    for char in line:
        if char == '<':
            break
        else:
            info = info + char
    return info

# Extracts all bins from bin field
def ExtractBIN(line: str):
    line = line.replace('[','')
    line = line.replace(']','')
    return line.split(',')

# Turns public variables into xml file
def ExportDataToXML(file_name):
    root = ET.Element("TruckInfo")
    truck_element = ET.Element("Truck")
    pallets_element = ET.Element("Pallets")
    root.append(truck_element)
    root.append(pallets_element)

    name_plate = ET.SubElement(truck_element,"NamePlate")
    load_capacity = ET.SubElement(truck_element,"LoadCapacity")
    weight = ET.SubElement(truck_element,"Weight")
    name_plate.text = TruckInfo.name_plate
    load_capacity.text = TruckInfo.load_capacity
    weight.text = TruckInfo.weight

    pallet: Pallet

    for pallet in AllPallets:
        pallet_element = ET.SubElement(pallets_element,"Pallet")
        pallet_goods = ET.SubElement(pallet_element,"Goods")
        pallet_BIN = ET.SubElement(pallet_element,"BIN")
        pallet_weight = ET.SubElement(pallet_element,"Weight")

        pallet_goods.text = pallet.goods
        pallet_BIN.text = pallet.BIN
        pallet_weight.text = pallet.weight

    tree = ET.ElementTree(root)
    with open(file_name,"wb") as files:
        tree.write(files)

if __name__=="__main__":
    print("Reading email file")
    ReadAllFile(DataFileName)
    print("Reading data from email file")
    ReadDataFromFile()
    print("Exporting data to XML file")
    ExportDataToXML(XMLFileName)
    print("Successfully completed")
    input("Press Enter to continue...")