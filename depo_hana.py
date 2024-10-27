import os
import time  # Import modul time untuk menambahkan delay
import sys  # Import sys untuk flush output
from dotenv import load_dotenv
from web3 import Web3

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Menghubungkan ke jaringan dengan RPC URL
RPC_URL = os.getenv('RPC_URL')
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Memastikan koneksi ke jaringan
if not web3.is_connected():
    print("Gagal terhubung ke jaringan.")
    exit()

# Private key dan alamat wallet
private_key = os.getenv('PRIVATE_KEY')
account = web3.eth.account.from_key(private_key)

# Alamat tujuan deposit
deposit_address = '0xC5bf05cD32a14BFfb705Fb37a9d218895187376c'  # Ganti dengan alamat yang sesuai

# ABI kontrak
contract_abi = [
    {
        "inputs": [],
        "name": "depositETH",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

# Membuat objek kontrak
contract = web3.eth.contract(address=deposit_address, abi=contract_abi)

def loading_animation(duration):
    """Fungsi untuk menampilkan animasi loading."""
    animation = ['-', '\\', '|', '/']
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in animation:
            sys.stdout.write(f'\r{frame} Mengirim transaksi...')
            sys.stdout.flush()
            time.sleep(0.1)  # Delay untuk animasi

def send_deposit(amount):
    try:
        # Menghitung jumlah dalam wei
        amount_in_wei = web3.to_wei(amount, 'ether')

        # Mengambil gas price terkini
        gas_price = web3.eth.gas_price  # Mengambil gas price otomatis dari jaringan

        # Mengatur gas limit (sesuaikan jika perlu)
        gas_limit = 100000

        # Membangun transaksi
        tx = contract.functions.depositETH().build_transaction({
            'from': account.address,
            'value': amount_in_wei,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': 8453  # ID jaringan Base Mainnet
        })

        # Menandatangani transaksi
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)

        # Menambahkan animasi saat mengirim transaksi
        loading_animation(2)  # Tampilkan animasi selama 5 detik

        # Mengirim transaksi
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"\nDeposit berhasil dikirim, transaksi hash:✅ {web3.to_hex(tx_hash)}")

        # Menunggu konfirmasi transaksi
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print("Deposit berhasil dikonfirmasi dalam block:✅", tx_receipt.blockNumber)

    except Exception as e:
        print("Kesalahan saat mengirim deposit:", e)

def main_menu():
    print("=====================================")
    print("=          DEPOSIT HANA             =")
    print("=        Created By 0xarvi          =")
    print("=====================================")
    print("Pilih opsi di bawah ini:")
    print("1.Mulai Deposit")
    print("2.Keluar")

    choice = input('Pilih opsi Anda: ')
    if choice == '1':
        amount = float(input('Masukkan jumlah yang ingin Anda depositkan (dalam ETH): '))
        print("Tekan Ctrl+C untuk menghentikan deposit.")
        try:
            while True:
                send_deposit(amount)
                time.sleep(5)  # Delay antara transaksi untuk menghindari masalah nonce
        except KeyboardInterrupt:
            print("\nDeposit dihentikan oleh pengguna.")
        except ValueError:
            print("Input tidak valid, pastikan Anda memasukkan angka yang benar.")
    elif choice == '2':
        print("Terima kasih")
    else:
        print("Opsi tidak valid, silakan coba lagi.")

# Menjalankan menu utama
if __name__ == "__main__":
    main_menu()
