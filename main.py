import pandas as pd
from pyzbar.pyzbar import decode
import cv2
from fpdf import FPDF

products = pd.DataFrame({
    'product_id': [1, 2, 3],
    'product_name': ['Apple', 'Banana', 'Milk'],
    'price': [0.50, 0.30, 1.20]
})

def get_product_details(product_id):
    product = products[products['product_id'] == product_id]
    if not product.empty:
        return product.iloc[0]['product_name'], product.iloc[0]['price']
    else:
        return None, None

def scan_qr_code():
    cap = cv2.VideoCapture(0)
    scanned_items = []

    print("Press 'q' to finish scanning.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        for barcode in decode(frame):
            product_id = int(barcode.data.decode('utf-8'))
            product_name, price = get_product_details(product_id)
            if product_name:
                print(f"Scanned: {product_name} - ${price}")
                scanned_items.append((product_name, price))
            else:
                print("Product not found!")
        
        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return scanned_items

def generate_invoice(scanned_items, shop_name="My Shop"):
    total = sum(price for _, price in scanned_items)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=shop_name, ln=True, align='C')
    pdf.cell(200, 10, txt="Invoice", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(100, 10, txt="Product", border=1)
    pdf.cell(40, 10, txt="Price", border=1, ln=True)

    for product_name, price in scanned_items:
        pdf.cell(100, 10, txt=product_name, border=1)
        pdf.cell(40, 10, txt=f"${price:.2f}", border=1, ln=True)

    pdf.ln(10)
    pdf.cell(100, 10, txt="Total", border=1)
    pdf.cell(40, 10, txt=f"${total:.2f}", border=1, ln=True)

    pdf.output("invoice.pdf")
    print("Invoice generated: invoice.pdf")

def main():
    print("Starting QR code scanner...")
    scanned_items = scan_qr_code()

    if scanned_items:
        print("Generating invoice...")
        generate_invoice(scanned_items)
    else:
        print("No items scanned. Exiting.")

if __name__ == "__main__":
    main()
