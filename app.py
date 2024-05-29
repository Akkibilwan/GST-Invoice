import streamlit as st
import pandas as pd

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

def display_invoice(business_details, billing_details, shipping_details, bank_details, items_df, total_invoice_amount):
    """Displays the formatted invoice."""
    st.header("GST Invoice")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Seller Details")
        st.write(f"**Name:** {business_details['business_name']}")
        st.write(f"**GSTIN:** {business_details['gst_number']}")
        st.write(f"**Address:** {business_details['address']}")

    with col2:
        st.subheader("Billing Details")
        st.write(f"**Name:** {billing_details['name']}")
        st.write(f"**GSTIN:** {billing_details['gst_number']}")
        st.write(f"**Address:** {billing_details['address']}")

    st.subheader("Shipping Details")
    st.write(f"**Name:** {shipping_details['name']}")
    st.write(f"**Address:** {shipping_details['address']}")

    st.subheader("Items")
    st.dataframe(items_df)

    st.subheader("Bank Details")
    st.write(f"**Bank Name:** {bank_details['bank_name']}")
    st.write(f"**Account Number:** {bank_details['account_number']}")
    st.write(f"**IFSC Code:** {bank_details['ifsc_code']}")

    st.subheader("Total Invoice Amount")
    st.write(f"**₹{total_invoice_amount:,.2f}**")

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
            display_invoice(business_details, billing_details, shipping_details, bank_details, items_df, total_invoice_amount)

if __name__ == "__main__":
    main()
