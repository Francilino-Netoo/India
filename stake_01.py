import re
import os
import time
import telebot
import pandas as pd
from kthread_sleep import sleep
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from db import TOKEN, USER_ID, message, count_falhas, cout_vela


bot = telebot.TeleBot(TOKEN)
user_id = USER_ID

driver = Driver(uc=True, headless=False) 

driver.get('https://stake.games/casino/games/crash')
sleep(1)

def obter_dataframe(query='*'):
    """Captura elementos da página e retorna como DataFrame"""
    df = pd.DataFrame()
    while df.empty:
        df = get_df(
            driver,
            By,
            WebDriverWait,
            EC,
            queryselector=query,
            with_methods=True,
        )
    return df

valores_capturados = set()
cont = 0

lista = []

while True:
    time.sleep(0.5)
    try:
        spans = driver.find_elements(By.XPATH, '//button[contains(@class, "variant-")]//span')
        
        for span in spans:
            valor = span.text.strip().replace("×", "").replace("x", "")  
            if valor and valor not in valores_capturados:
                valores_capturados.add(valor)
                
                try:
                    
                    numero = float(valor.replace('.', '').replace(',', '.'))
                    print(f"📌 Result: {numero}")
                    lista.append(numero)
                    
                    if len(lista) > count_falhas:
                        lista.pop(0)
                    
                    if numero < float(cout_vela):
                        cont += 1
                        
                        if cont == count_falhas - 1:
                            alerta_msg = f"⚠️ Alert! Only 1 more to reach the limit of {count_falhas}..\n\n📈 Last value: {numero}x"
                            alerta = bot.send_message(user_id, alerta_msg, parse_mode='HTML', disable_web_page_preview=True)

                    else:
                        try:
                            bot.delete_message(user_id, alerta.message_id)
                        except:
                            pass
                        cont = 0
                    
                    if cont == count_falhas:
                        try:
                            bot.delete_message(user_id, alerta.message_id)
                        except:
                            pass
                        cont = 0
                        
                        print('Atenção: encontrou o sinal')
                        msg = f"{message}\n\n📈 {numero}x 📉\n\nResults: {lista}"
                        bot.send_message(user_id, msg, parse_mode='HTML', disable_web_page_preview=True)

                except ValueError:
                    print(f"⚠️ Valor inválido: {valor}")

    
    except Exception as e:
        pass
