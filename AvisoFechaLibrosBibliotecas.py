# Primero intenté usar webscraping; pero hacer login no era fácil.
# Por eso el plan B ha sido enviar eventos de teclado y ratón para emular lo que hago a mano,
# y usar el portapapeles para capturar el texto de la página.
#   https://github.com/asweigart/pyautogui

import csv  
import pyautogui;
import subprocess;
import time;
import os;
from tkinter import Tk
from collections import namedtuple


def main():

    SUser = namedtuple('SUserData', ['name', 'books'])
    users = [];

    with open('users.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:                
                books = getBooks(row[0], row[1], row[2])
                user = SUser(row[0], books);
                users.append(user)
                line_count += 1
        print(f'Processed {line_count} lines.')


    sendMail(users)



def getBooks(name, user, pwd):

   # AVISO al llamar a "pyautogui.hotkey()" usar letras ¡minúsculas!
    subprocess.call(['C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe', 'https://www.katalogoak.euskadi.eus/cgi-bin_q81a/abnetclop?SUBC=GIP/G0300'])
    time.sleep(4) # segundos
    # Coordenadas input de usuario
    pyautogui.moveTo(900, 195) # Move the mouse to the x, y coordinates
    pyautogui.click() # Click the mouse at its current location.
    pyautogui.write(user, interval=0.05)
    pyautogui.press('tab')
    pyautogui.write(pwd, interval=0.05)
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(1) # segundos
    # Clikcar vínculo "Nire biblioteka"
    pyautogui.moveTo(1100, 175) # Move the mouse to the x, y coordinates
    pyautogui.click()
    time.sleep(1) # segundos
    # Bajar para ver los libros prestados
    pyautogui.press('down', presses=10)
    time.sleep(1) # segundos

    pyautogui.alert('Una vez veas los libros prestados en pantalla, pulsa OK.')
    
    # Copiar contenido al portapapeles    
    pyautogui.hotkey('ctrl', 'a', interval = 0.15) # Select ALL
    pyautogui.hotkey('ctrl', 'c', interval = 0.15) # Copy
    
    # Leer texto del portapapeles
    root = Tk()
    # Ocultar la ventana de Tk que se crea
    root.withdraw()
    text = root.clipboard_get()
    start = text.find('Maileguak')
    end = text.find('Desideratak')    

    books = (text[start : end]).splitlines()
       
    print(f'Books for {name} saved')
    for book in books:
        print(f'{book}')
        
    time.sleep(1) # segundos
    pyautogui.hotkey('ctrl', 'w') # Press the Ctrl-W hotkey combination.
    time.sleep(1) # segundos
    
    return books



# https://www.youtube.com/watch?v=JRCJ6RtE3xU
def sendMail(users):

    import csv
    import os
    import email, smtplib, ssl
    import imghdr
    from datetime import date
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from datetime import datetime
    
    to_emails = []

    with open('mail.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 1:
                    FROM_EMAIL_ADDRESS = row[0]
                    FROM_EMAIL_PASSWORD = row[1]
                    to_emails.append(row[0])
                elif line_count > 1:
                    to_emails.append(row[0]) 
                line_count += 1



    # email object that has multiple part:
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL_ADDRESS   
    msg['To'] = ','.join(to_emails)
    msg['Subject'] = 'Liburutegia ' + date.today().strftime('%Y-%m-%d')

    users_html = ''

    for user in users:
        users_html += f'<h1>{user.name}:</h1>\n'
        users_html += '<table border="1">\n'
        
        for book in user.books:
            columns = book.split('\t')
            if len(columns) > 2:            
                users_html += '<tr>'
                for i_column, column in enumerate(columns):
                    if i_column > 0 and i_column < 5:
                        if i_column == 3 and column.find('/') >= 0:
                           # Si hay espacios delante, o detrás; no funciona datetime.strptime()
                           column = column.strip()
                           book_date = datetime.strptime(column, '%d/%m/%Y')
                           column = book_date.strftime('%Y-%m-%d %A')
                           today_date = datetime.today();
                           delta_date = book_date - today_date;
                           if delta_date.days < 7:
                              users_html += f'<td style="background-color:#ff0000">{column}</td>'
                           else:
                              users_html += f'<td>{column}</td>'                              
                        else:
                           users_html += f'<td>{column}</td>'

                users_html += '</tr>\n'

        users_html += '</table>\n'

    html = f"""\
    <html>
      <body>
        <p>Liburutegian ditugun maileguak</p>
        {users_html}
      </body>
    </html>
    """

    #print(html)

    part2 = MIMEText(html, "html")
    msg.attach(part2)


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(FROM_EMAIL_ADDRESS, FROM_EMAIL_PASSWORD)
        smtp.send_message(msg)
    

if __name__ == '__main__':
    main()
