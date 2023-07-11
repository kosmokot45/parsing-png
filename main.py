from PIL import Image

def convertImage(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines_new = ''
        for v in lines:
            lines_new += hex(int(v.rstrip()))[2:]
    return lines_new

def readByte(filename):
    with open(filename, 'rb') as file:
        lines = file.readlines()
        new_dat = ''
        for v in lines:
            if str(v).startswith('b\'//') or str(v).startswith('b\'x'):
                continue
            v = int(v, 2)
            v = hex(v)
            new_dat += str(v)[2:]
    return new_dat

def pngCoderEncoder(filename, mode, filename_w='', lines='', filename_o=''):
    with open(filename,'rb') as pngf:
        stroka = pngf.read().hex()

    cursor_0 = 0
    start = cursor_0
    stop = cursor_0+(8*2)
    cursor_0 = stop
    if stroka[start:stop] != "89504e470d0a1a0a":
        print("signature fail")

    new_file = stroka[start:stop]
    
    data_to_fpga = ''

    flag_idat = 0

    read = True
    while read:
        start = cursor_0
        stop = cursor_0+(4*2)
        cursor_0 = stop
        s = stroka[start:stop]
        chunkDataLength = int(stroka[start:stop],16)
        chunkDataLengthStr = stroka[start:stop]

        start = cursor_0
        stop = cursor_0+8
        cursor_0 = stop
        s = stroka[start:stop]
        chunkType= bytes.fromhex(stroka[start:stop]).decode('ANSI', 'ignore')
        chunkTypeStr = stroka[start:stop]

        start = cursor_0
        stop = cursor_0+(chunkDataLength*2)
        cursor_0 = stop
        chunkDataHexStr = stroka[start:stop]

        start = cursor_0
        stop = cursor_0+(4*2)
        cursor_0 = stop
        chunkCrcHexStr = stroka[start:stop]
        

        if chunkType == 'IDAT':
            flag_idat = 1
            if mode == 'from_fpga':
                new_file += lines
            elif mode == 'to_fpga':
                data_to_fpga += chunkDataHexStr

        if chunkType == 'IEND':
            read = False
            if mode == 'from_fpga':
                with open('res.png', 'wb') as res:
                    for el in range(0, len(new_file), 2):
                        start = el
                        stop = el + 2
                        b = int(new_file[start:stop],16).to_bytes(1,byteorder='big')
                        res.write(b)
            elif mode == 'to_fpga':
                with open(filename_w, 'w') as file:
                    for el in range(0, len(data_to_fpga), 2):
                        start = el
                        stop = el + 2
                        file.write(data_to_fpga[start:stop] + '\n')
                    return

def convert2gray(filename):
    img = Image.open(filename).convert('L')
    img.save('greyscale.png')

def prepare2fpga(filename):
    pass

def main():
    filename = 'cakes.jpg'
    convert2gray(filename)
    filename_gs = 'greyscale.png'
    pngCoderEncoder(filename_gs, 'to_fpga', filename_w='data_to_fpga.txt')


if __name__ == '__main__':
    main()