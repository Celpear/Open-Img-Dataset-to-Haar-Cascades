import os
import xml.etree.ElementTree as ET
import os
import argparse

def create_xml(image_path, object_info, output_folder):
    root = ET.Element("annotation")

    folder = ET.SubElement(root, "folder")
    folder.text = os.path.dirname(image_path)

    filename = ET.SubElement(root, "filename")
    filename.text = os.path.basename(image_path)

    path = ET.SubElement(root, "path")
    path.text = image_path

    source = ET.SubElement(root, "source")
    database = ET.SubElement(source, "database")
    database.text = "Unknown"

    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    height = ET.SubElement(size, "height")
    depth = ET.SubElement(size, "depth")

    size_info = object_info["size"]
    width.text = str(size_info["width"])
    height.text = str(size_info["height"])
    depth.text = str(size_info["depth"])

    segmented = ET.SubElement(root, "segmented")
    segmented.text = "0"

    object_info = object_info["object"]
    object_elem = ET.SubElement(root, "object")
    name = ET.SubElement(object_elem, "name")
    pose = ET.SubElement(object_elem, "pose")
    truncated = ET.SubElement(object_elem, "truncated")
    difficult = ET.SubElement(object_elem, "difficult")
    bndbox = ET.SubElement(object_elem, "bndbox")

    name.text = object_info["name"]
    pose.text = object_info["pose"]
    truncated.text = str(object_info["truncated"])
    difficult.text = str(object_info["difficult"])

    bbox_info = object_info["bndbox"]
    xmin = ET.SubElement(bndbox, "xmin")
    ymin = ET.SubElement(bndbox, "ymin")
    xmax = ET.SubElement(bndbox, "xmax")
    ymax = ET.SubElement(bndbox, "ymax")

    xmin.text = str(bbox_info["xmin"])
    ymin.text = str(bbox_info["ymin"])
    xmax.text = str(bbox_info["xmax"])
    ymax.text = str(bbox_info["ymax"])

    # Sicherstellen, dass der Ausgabeordner existiert
    os.makedirs(output_folder, exist_ok=True)

    tree = ET.ElementTree(root)
    output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(image_path))[0] + ".xml")
    tree.write(output_path)

def main(pos_file_path,object_name,img_width):
    # Pfad ohne Dateinamen erstellen
    dir_path = os.path.dirname(pos_file_path)
    output_folder = "annotations"

    with open(pos_file_path, "r") as file:
        for line in file:
            parts = line.strip().split()
            image_path = parts[0]
            object_info = {
                "size": {"width": img_width, "height": img_width, "depth": 3},
                "object": {
                    "name": str(object_name),
                    "pose": "Unspecified",
                    "truncated": 0,
                    "difficult": 0,
                    "bndbox": {
                        "xmin": float(parts[1]),
                        "ymin": float(parts[2]),
                        "xmax": float(parts[3]),
                        "ymax": float(parts[4]),
                    }
                }
            }
            create_xml(image_path, object_info, dir_path+"/"+output_folder)

if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--pos_file_path', help='Path to the pos.txt file.', required=True)
    parser.add_argument('--object_name', help='Name of the detected Object', required=True)
    parser.add_argument('--w', help='Width and height of the image', required=False)
    
    args = parser.parse_args()
    if args.w == None:
        img_width = 2000
    else:
        img_width = args.w
    main(args.pos_file_path,args.object_name,img_width)
