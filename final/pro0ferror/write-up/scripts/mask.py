from PIL import Image, ImageOps

QR_SIZE = 41      # QR Code size, based on version
BORDER  = 30      # Border size, in pixels
WIDTH   = 675     # Total width  of the 'paper' including the border, in pixels
LENGTH  = 675     # Total length of the 'paper' including the border, in pixels

def GenerateCustomMask():
    """Generate our custom mask pattern with j%2 == 0.
    Saves output as 'custom-mask.png'.
    """
    image = Image.new('L', (QR_SIZE, QR_SIZE))
    for j in range(0, QR_SIZE): # Rows
        for i in range(0, QR_SIZE): # Columns
            if j % 2 == 0:
                image.putpixel((j, i), 0)
            else:
                image.putpixel((j, i), 255)

    image = image.resize((WIDTH-2*BORDER, LENGTH-2*BORDER), Image.NEAREST)  # Resize to the 'paper' size
    image = ImageOps.expand(image, border=30, fill=255)                     # Add white borders to match the 'paper' size
    
    output_path = './assets/custom-mask.png'

    print('[+] Saving custom mask as "{}"'.format(output_path))   
    image.save(output_path)

def ApplyMask(input_path, mask_path, output_path):
    """Remove the mask pattern from the QR code.
    Needs 'mask.png', 'paper.png' and mask-protect.png to be generated first.
    Saves output as 'raw_qr.png'.
    """
    # Crop to remove border
    mask = Image.open(mask_path).crop((BORDER, BORDER, WIDTH-BORDER, LENGTH-BORDER)).convert('L')
    qrcode = Image.open(input_path).crop((BORDER, BORDER, WIDTH-BORDER, LENGTH-BORDER)).convert('L')

    protection = Image.open('./assets/mask-protect.png').crop((BORDER, BORDER, WIDTH-BORDER, LENGTH-BORDER))     # Mode 'RGBA'

    # Create and fill new image
    new_im = Image.new(mode='1', size=(WIDTH-2*BORDER, LENGTH-2*BORDER))

    for x in range(0, WIDTH-2*BORDER):
        for y in range(0, LENGTH-2*BORDER):
            is_protected = (protection.getpixel((x, y))[3] != 0)                    # Transparent = protected pixel

            if is_protected:
                new_px = qrcode.getpixel((x, y))                                    # Only apply mask if not protected
            else:
                is_masked = (mask.getpixel((x, y)) == 255)                          # Check if pixel is masked
                
                if is_masked:                                     
                    new_px = qrcode.getpixel((x, y)) ^ mask.getpixel((x, y))        # XOR with mask
                    new_px = 255 - new_px                                           # Invert black/white for no apparent reason...
                else:
                    new_px = qrcode.getpixel((x, y))                                # Protected pixel, don't change
                    new_px = 255 - new_px                                           # Invert black/white for no apparent reason...

            # For grey bits (custom mask), make them white instead of grey
            if new_px not in [0, 255]:
                new_px = 0

            new_im.putpixel((x, y), new_px)                                         # Put final pixel

    new_im = ImageOps.expand(new_im, border=30, fill=255)                           # Add white borders

    print('[+] Saving QR code as "{}"'.format(output_path))                         # Save raw QR code
    new_im.save(output_path)

def main():
    GenerateCustomMask()
    # Remove custom mask from the QR code
    ApplyMask('./assets/paper.png', './assets/custom-mask.png', output_path='./assets/raw-qr.png')

if __name__ == '__main__':
    main()