import getpass
import sys

def encoder(data):
    """
    Fungsi ini untuk encode str atau list menjadi bentuk ordinal
    @param data: string panjang atau list
    @type data: str or list or tuple
    @return: encoded string
    @rtype: str
    """
    result = []
    if isinstance(data, str):
        data = data.strip().split(" ")
    for datum in data:
        temp = []
        for x in datum:
            temp.append(str(ord(x)))
        result.append('+'.join(temp))
    return ' '.join(result)


def interactive(mode='r', filename=''):
    """
    Interactive mode untuk enkripsi
    @param mode: r -> read | w -> write
    @type mode: str
    @param filename: name of output file
    @type filename: str
    """
    postgres = {
        "1": "Alias\t: ",
        "2": "Nama Database\t: ",
        "3": "Instance Database / Host\t: ",
        "4": "Username\t: ",
        "5": "Password \t: ",
        "6": "Port (ex:5432)\t: ",
        "7": "Schema (ex:public)\t: "
    }
    data = {}
    status = True
    while status:
        print('Selamat datang di Common Library-Encoder')
        print('1. Postgres\n\n99. Exit')
        try:
            source = int(input('Masukan pilihan Anda [1,99]: ')) or 9999
            if source == 1:
                status = False
                conf = postgres
                print('\nKonfigurasi Database: ')
                idx = 0
                for (k, v) in conf.items():
                    if v.startswith('Password'):
                        data.update({k: getpass.getpass(f'{idx + 1}. {v}') or ' '})
                    else:
                        data.update({k: str(input(f'{idx + 1}. {v}')) or ' '})
                    idx+=1
                result = [item for k, item in sorted(data.items())]
                config = encoder(result)
                print(f'\nKonfigurasi:\n{config}')
                if mode == 'w':
                    try:
                        file = open(f'{filename}', 'w')
                        file.write(config)
                        file.close()
                    except OSError:
                        print('Terjadi kesalahan saat menyimpan konfigurasi.')
            elif source == 99:
                print('\nProgram berhasil berhenti')
                sys.exit()
            else:
                print('Pilihan tidak tersedia salah!')
        except ValueError:
            print('Input berupa angka!\n')
        except KeyboardInterrupt:
            print('\nProgram berhasil berhenti')
            sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        interactive()
    elif len(sys.argv) == 3:
        if sys.argv[1] == '-o':
            interactive('w', str(sys.argv[2]))
    else:
        print('Usage: python encoder.py [-o filename]')