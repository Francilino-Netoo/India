import json
import time
import websocket

def on_message(ws, message):
    print(message)

def on_open(ws):
    print('Conexão aberta')
    #mensagem1 = {"adjust_start_time":1,"count":5000,"end":"latest","style":"ticks","subscribe":1,"ticks_history":"R_100","req_id":1}
    #json_message1 = json.dumps(mensagem1)
    #ws.send(json_message1)
    

def on_close(ws, close_status_code, close_msg):
    print(f"Conexão fechada: {close_status_code}, {close_msg}")
    time.sleep(1)
    reconectar_ws(ws)

def on_error(ws, error):
    print(f"Erro: {error}")
    time.sleep(1)
    reconectar_ws(ws)

def reconectar_ws(ws):
    print("Tentando reconectar...")
    ws.run_forever()

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://arbmastersocket.multivirtus.com",
                                on_message=on_message,
                                on_open=on_open,
                                on_close=on_close,
                                on_error=on_error)
    ws.run_forever()
