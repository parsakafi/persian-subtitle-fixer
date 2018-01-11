'''
Persian Subtitle Fixer
Author: Parsa Kafi (http://parsa.ws)
Version: 1.1
'''

import os
import sys
import shutil
import time
targetFormat = 'UTF-16'
supportFile = ['.srt','.smi']

# Source: https://stackoverflow.com/a/45167602/3224296
def predict_encoding(file_path, n_lines=20):
    '''Predict a file's encoding using chardet'''
    import chardet
    # Open the file as binary data
    with open(file_path, 'rb') as f:
        # Join binary lines for specified number of lines
        rawdata = b''.join([f.readline() for _ in range(n_lines)])
    return chardet.detect(rawdata)['encoding']
    
def subtitle_fixer(arg):
    """
    Subtitle Fixer
    Change encoding file & replace arabic character

    Parameters
    ----------
    arg : array
        sys.argv
    """
    if len(arg) > 1:
        fileName = arg[1]
        backup = arg[2] if len(arg) == 3 else True
    else:
        help()
        return
    if not os.path.exists(fileName) or not os.path.isfile(fileName):
        print('File input not exists!')
        pause()
        return
    
    file = os.path.splitext(os.path.basename(fileName))
    if not file[1].lower() in supportFile:
        print('Your file is not subtitle file! (' + ', '.join(supportFile).upper() + ')')
        pause()
        return
    
    outputDir = os.path.dirname(os.path.abspath(fileName))
    newfilename = outputDir + '\\' + file[0] + '.backup' + file[1]
    # Create a backup from file
    shutil.copy(fileName, newfilename)
    
    try:
        format = predict_encoding(fileName)
        print("Converting file: '" + file[0] + file[1] + "'")
        save_subtitle(newfilename,fileName,format,targetFormat)
        if backup == '-b':
            os.remove(newfilename)
        print('Done.')
        time.sleep(2)
    #except Exception as e: print(e)
    except:
        print("Error: failed to convert '" + file[0] + file[1] + "'.")
        pause()
        
def save_subtitle(filename, newFilename, encoding_from, encoding_to='UTF-16'):
    """
    Save subtitle with new encoding

    Parameters
    ----------
    filename : str
        Current file
    newFilename : str
        New file with change
    encoding_from : str
        Current file encoding
    encoding_to : str
        New file encoding  
    """
    print('Encoding from: ' + encoding_from + ' to ' + encoding_to)
    fr = open(filename, 'r') if encoding_from == 'MacCyrillic' else open(filename, 'r', encoding=encoding_from)
    with open(newFilename, 'w', encoding=encoding_to) as fw:
        for line in fr:
            str = replace_arabic(line[:-1])
            fw.write(str +'\n')

def replace_arabic(str):
    """
    Replace arabic character with farsi/persian character

    Parameters
    ----------
    str : str
        Input letter

    Returns
    -------
    str
        Persian character letter
    """
    ar = ['ي', 'ك', '٤', '٥', '٦', 'ة']
    fa = ['ی', 'ک', '۴', '۵', '۶', 'ه']
    for i in range(len(ar)):
        str = str.replace(ar[i],fa[i])
    return str
    
def pause():
    programPause = input("\nPress the <ENTER> key to continue...")
    
def help():
    help = "Persian Subtitle Fixer\nAuthor: Parsa Kafi (http://parsa.ws)\n\n" \
        "Usage:\n" \
        "\tpersian-subtitle-fixer subtitle_file.srt\n" \
        "Disable create backup file:\n" \
        "\tpersian-subtitle-fixer subtitle_file.srt -b"
    print(help)
    pause()
    
if __name__ == '__main__':
    subtitle_fixer(sys.argv)