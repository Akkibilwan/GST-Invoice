import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Set up page configuration
st.set_page_config(page_title="GST Invoice Generator", layout="wide")

# Define functions
def calculate_total(df):
    """Calculates total amount for each item and total invoice amount."""
    df['Total Amount'] = df['Rate'] * df['Quantity']
    df['CGST Amount'] = df['Total Amount'] * (df['CGST'] / 100)
    df['SGST Amount'] = df['Total Amount'] * (df['SGST'] / 100)
    df['Final Amount'] = df['Total Amount'] + df['CGST Amount'] + df['SGST Amount']
    total_invoice_amount = df['Final Amount'].sum()
    return df, total_invoice_amount

def generate_pdf(business_details, billing_details, shipping_details, bank_details, items_df, total_invoice_amount):
    """Generates a PDF invoice."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Invoice title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "GST Invoice")

    # Seller details
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, "Seller Details:")
    c.drawString(50, 680, f"Name: {business_details['business_name']}")
    c.drawString(50, 660, f"GSTIN: {business_details['gst_number']}")
    c.drawString(50, 640, f"Address: {business_details['address']}")

    # Billing details
    c.drawString(400, 700, "Billing Details:")
    c.drawString(400, 680, f"Name: {billing_details['name']}")
    c.drawString(400, 660, f"GSTIN: {billing_details['gst_number']}")
    c.drawString(400, 640, f"Address: {billing_details['address']}")

    # Shipping details
    c.drawString(50, 600, "Shipping Details:")
    c.drawString(50, 580, f"Name: {shipping_details['name']}")
    c.drawString(50, 560, f"Address: {shipping_details['address']}")

    # Items table
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 530, "Items")
    c.setFont("Helvetica", 10)
    c.drawString(50, 510, "Description | HSN Code | Rate | Quantity | Unit | CGST | SGST | Final Amount")

    y = 490
    for index, row in items_df.iterrows():
        c.drawString(50, y, f"{row['Description']} | {row['HSN Code']} | {row['Rate']:.2f} | {row['Quantity']} | {row['Unit']} | {row['CGST']:.2f} | {row['SGST']:.2f} | {row['Final Amount']:.2f}")
        y -= 15

    # Bank details
    c.setFont("Helvetica", 12)
    c.drawString(50, y - 30, "Bank Details:")
    c.drawString(50, y - 50, f"Bank Name: {bank_details['bank_name']}")
    c.drawString(50, y - 70, f"Account Number: {bank_details['account_number']}")
    c.drawString(50, y - 90, f"IFSC Code: {bank_details['ifsc_code']}")

    # Total invoice amount
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 120, "Total Invoice Amount:")
    c.drawString(50, y - 140, f"₹{total_invoice_amount:,.2f}")

    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    return pdf_bytes

def main():
    """Main function to run the Streamlit app."""

    st.title("GST Invoice Generator")

    # Business details
    business_details = {}
    business_details['business_name'] = st.text_input("Business Name")
    business_details['gst_number'] = st.text_input("GSTIN")
    business_details['address'] = st.text_area("Address")

    # Billing details
    billing_details = {}
    billing_details['name'] = st.text_input("Customer Name")
    billing_details['gst_number'] = st.text_input("Customer GSTIN (Optional)")
    billing_details['address'] = st.text_area("Customer Address")

    # Shipping details
    shipping_details = {}
    shipping_details['name'] = st.text_input("Shipping Name")
    shipping_details['address'] = st.text_area("Shipping Address")

    # Bank details
    bank_details = {}
    bank_details['bank_name'] = st.text_input("Bank Name")
    bank_details['account_number'] = st.text_input("Account Number")
    bank_details['ifsc_code'] = st.text_input("IFSC Code")

    # Items table
    items_df = pd.DataFrame(columns=['Description', 'HSN Code', 'Rate', 'Quantity', 'Unit', 'CGST', 'SGST'])

    # Add item button
    add_item = st.button("Add Item")
    if add_item:
        new_item = {}
        new_item['Description'] = st.text_input("Description", key="description")
        new_item['HSN Code'] = st.text_input("HSN Code", key="hsn_code")
        new_item['Rate'] = st.number_input("Rate", value=0.0, format="%.2f", key="rate")
        new_item['Quantity'] = st.number_input("Quantity", value=1, key="quantity")
        new_item['Unit'] = st.text_input("Unit", key="unit")
        new_item['CGST'] = st.number_input("CGST (%)", value=0.0, format="%.2f", key="cgst")
        new_item['SGST'] = st.number_input("SGST (%)", value=0.0, format="%.2f", key="sgst")
        items_df = pd.concat([items_df, pd.DataFrame([new_item])], ignore_index=True)

    # Generate Invoice button
    if st.button("Generate Invoice"):
        if items_df.empty:
            st.warning("Please add items to the invoice.")
        else:
            items_df, total_invoice_amount = calculate_total(items_df.copy())
            pdf_bytes = generate_pdf(business_details, billing_details, shipping_details, bank_details, items_df, total_invoice_amount)
            st.download_button("Download Invoice", data=pdf_bytes, file_name="invoice.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
