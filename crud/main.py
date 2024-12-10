import csv
import os

CLIENT_SCHEMA = ['name', 'company', 'email', 'position']
CLIENT_TABLE = '.clients.csv'
clients = []

def create_client(client):
    global clients

    if client not in clients:
        clients.append(client)
    else:
        print("Client already in client's list")

def list_clients():
    print('uid |  name  | company  | email  | position ')
    print('*' * 50)

    for idx, client in enumerate(clients):
        print('{uid} | {name} | {company} | {email} | {position}'.format(
            uid=idx,
            name=client['name'],
            company=client['company'],
            email=client['email'],
            position=client['position']))

def update_client(client_id, updated_client):
    global clients

    if 0 <= client_id < len(clients):
        clients[client_id] = updated_client
    else:
        print("Client not in client's list")

def delete_client(client_id):
    global clients

    if 0 <= client_id < len(clients):
        del clients[client_id]
    else:
        print("Client ID out of range")

def search_client(client_name):
    for client in clients:
        if client['name'] == client_name:
            return True
    return False

def _get_client_field(field_name, message='What is the client {}?'):
    field = None

    while not field:
        field = input(message.format(field_name))

    return field

def _get_client_from_user():
    client = {
        'name': _get_client_field('name'),
        'company': _get_client_field('company'),
        'email': _get_client_field('email'),
        'position': _get_client_field('position'),
    }

    return client

def _initialize_clients_from_storage():
    if os.path.exists(CLIENT_TABLE):
        with open(CLIENT_TABLE, mode='r') as f:
            reader = csv.DictReader(f, fieldnames=CLIENT_SCHEMA)
            for row in reader:
                clients.append(row)
    else:
        print(f"El archivo {CLIENT_TABLE} no existe. Iniciando una lista vacía.")

def _save_clients_to_storage():
    tmp_table_name = f'{CLIENT_TABLE}.tmp'
    try:
        # Elimina el archivo temporal si ya existe
        if os.path.exists(tmp_table_name):
            os.remove(tmp_table_name)
        
        with open(tmp_table_name, mode='w') as f:
            writer = csv.DictWriter(f, fieldnames=CLIENT_SCHEMA)
            writer.writerows(clients)
        
        os.rename(tmp_table_name, CLIENT_TABLE)
    except Exception as e:
        print(f"Error al guardar los clientes: {e}")
        if os.path.exists(tmp_table_name):
            os.remove(tmp_table_name)


def _print_welcome():
    print('WELCOME TO PLATZI VENTAS')
    print('*' * 50)
    print('What would you like to do today?:')
    print('[C]reate client')
    print('[L]ist clients')
    print('[U]pdate client')
    print('[D]elete client')
    print('[S]earch client')

if __name__ == '__main__':
    _initialize_clients_from_storage()
    _print_welcome()

    command = input().upper()

    if command == 'C':
        client = _get_client_from_user()
        create_client(client)
    elif command == 'L':
        list_clients()
    elif command == 'U':
        try:
            client_id = int(_get_client_field('id'))
            if 0 <= client_id < len(clients):
                updated_client = _get_client_from_user()
                update_client(client_id, updated_client)
            else:
                print("Client ID out of range")
        except ValueError:
            print("El ID debe ser un número entero.")
    elif command == 'D':
        try:
            client_id = int(_get_client_field('id'))
            if 0 <= client_id < len(clients):
                delete_client(client_id)
            else:
                print("Client ID out of range")
        except ValueError:
            print("El ID debe ser un número entero.")
    elif command == 'S':
        client_name = _get_client_field('name')
        found = search_client(client_name)

        if found:
            print("The client is in the client's list")
        else:
            print(f"The client: {client_name} is not in our client's list")
    else:
        print("Invalid command")

    _save_clients_to_storage()
