from TelegramBot import main_TelegramBot


if __name__ == '__main__':
    try:
        print('Ejecutando Aplicacion')
        
        while True:
            main_TelegramBot()
    except KeyboardInterrupt:
        exit()