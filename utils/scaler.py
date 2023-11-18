from PIL import Image, ImageOps, ImageDraw

def padAndSaveImage(original_pfad, ziel_pfad, ziel_groesse):
    # Öffne das Bild
    bild = Image.open(original_pfad)
    # Skaliere das Bild, füge schwarze Ränder hinzu und zentriere es
    #skaliertes_bild = ImageOps.pad(bild, ziel_groesse, method=0, bleed=0.0, centering=(0.5, 0.5))
    skaliertes_bild = ImageOps.pad(bild, ziel_groesse)
    # Speichere das skalierte Bild
    skaliertes_bild.save(ziel_pfad)


def translateBoxes(box_pos, img_path, target_size, debug=False):
    box_pos = box_pos.split()
    image = Image.open(img_path)

    # Original image size
    original_width = image.width
    original_height = image.height

    # Original box positions
    original_box_left = float(box_pos[1])
    original_box_top = float(box_pos[2])
    original_box_right = float(box_pos[3])
    original_box_bottom = float(box_pos[4])

    # Target size
    target_width, target_height = target_size

    # Calculate the center
    original_center_height = original_height / 2

    # Scaling factor
    pad_scale = target_width / original_width

    # Calculate top position
    original_normalized_top_pos = original_box_top - original_center_height
    new_top_pos = (original_normalized_top_pos * pad_scale) + (target_height / 2)

    # Calculate bottom position
    original_normalized_bottom_pos = original_box_bottom - original_center_height
    new_bottom_pos = (original_normalized_bottom_pos * pad_scale) + (target_height / 2)

    # Calculate the scaling factors for the box positions
    scaling_factor_width = target_width / original_width

    # Calculate the new box positions for the scaled image
    new_box_left = original_box_left * scaling_factor_width
    new_box_right = original_box_right * scaling_factor_width

    # Create a new box for the scaled image
    new_box_pos = [box_pos[0],new_box_left, new_top_pos, new_box_right, new_bottom_pos]
    if debug:
        new_box_pos_debug = [new_box_left, new_top_pos, new_box_right, new_bottom_pos]
        old_box_pos_debug = [original_box_left, original_box_top, original_box_right, original_box_bottom]

        # Draw new image
        # Apply the padding operation
        scaled_image = ImageOps.pad(image, target_size)

        # Draw the box on the scaled image
        draw = ImageDraw.Draw(scaled_image)
        draw.rectangle(new_box_pos_debug, outline="red", width=2)

        # Display the scaled image with the box
        # Draw the old image
        draw2 = ImageDraw.Draw(image)
        draw2.rectangle(old_box_pos_debug, outline="red", width=2)

        image.show()
        scaled_image.show()

    return new_box_pos
