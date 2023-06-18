from PIL import Image

class AsciiImage:
    """ Ascii representation of an image """

    CHAR_LEVELS = " ░▒▓█"
    """ Char lights levels for pixel to ascii (darker to lighter)"""
    MAX_SIZE = 100
    """ Max size of the image (height and width) """
    ASCII_CHAR_WIDTH = 2
    """ Number of ascii chars to make a pixel """

    def __init__(self, image_file):
        self._image_file = image_file
        self._ascii = self._parse_ascii_image()

    def _parse_ascii_image(self, size=(0,0)) -> str:
        """ Parse image as ascii 
        Params:
            - size : [tuple (int, int)] out size of the ascii
        """
        image_in = Image.open(self._image_file)

        # process image for ascii usage (resize & convert)
        image_gb = image_in.convert('L')
        if size == (0,0):
            width,height = image_in.size
            if width > AsciiImage.MAX_SIZE or height > AsciiImage.MAX_SIZE:
                scale_factor = AsciiImage.MAX_SIZE / max(width, height)
                image_gb = image_gb.resize((int(width * scale_factor), int(height * scale_factor)))
        else:
            image_gb = image_gb.resize(size)

        # convert to ascii
        width, height = image_gb.size
        ascii_str = ""
        for pixel_y in range(height):
            for pixel_x in range(width):
                pixel = image_gb.getpixel((pixel_x, pixel_y))
                char_level = int(pixel / 255 * (len(AsciiImage.CHAR_LEVELS) - 1))
                char = AsciiImage.CHAR_LEVELS[char_level]
                ascii_str += char * AsciiImage.ASCII_CHAR_WIDTH
            ascii_str += '\n'
        return ascii_str

    def get_resized_ascii(self, target_width, target_height) -> str:
        """ Return a resized ascii representation of this image"""
        return self._parse_ascii_image(size=(target_width, target_height))

    def get_ascii(self) -> str:
        """ Return native ascii representation of this image """
        return self._ascii
