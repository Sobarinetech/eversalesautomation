import streamlit as st
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure the Google API Key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Personalized Sales Proposal Generator")
st.write("Fill out the form below to receive a personalized sales proposal.")

# Contact form
with st.form("contact_form"):
    name = st.text_input("Full Name", max_chars=50, placeholder="Enter your full name")
    email = st.text_input("Email Address", max_chars=50, placeholder="Enter your email")
    phone = st.text_input("Phone Number", max_chars=15, placeholder="Enter your phone number")
    product = st.selectbox("Select Product", ["Product A", "Product B", "Product C", "Product D"])
    additional_info = st.text_area("Additional Information", placeholder="Provide any specific requirements or details")

    # Submit button
    submit_button = st.form_submit_button("Submit")

# Process form submission
if submit_button:
    if name and email and product:
        try:
            # Generate personalized sales proposal using AI
            prompt = f"Generate a personalized sales proposal for {name} regarding {product}. Include details about its benefits, pricing, and how it solves common problems. Additional details: {additional_info}"
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            proposal_text = response.text

            # Display the generated proposal on the UI
            st.success("Sales proposal generated successfully!")
            st.write("Generated Sales Proposal:")
            st.write(proposal_text)

            # Email configuration
            sender_email = "your_email@example.com"  # Replace with your email
            sender_password = st.secrets["EMAIL_PASSWORD"]  # Add this secret to Streamlit's secrets
            recipient_email = email

            # Email message setup
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Personalized Sales Proposal for {product}"
            message["From"] = sender_email
            message["To"] = recipient_email

            # Add the proposal text to the email body
            email_body = f"""
            Hi {name},

            Thank you for your interest in {product}. Please find below your personalized sales proposal:

            {proposal_text}

            If you have any questions or need further assistance, feel free to reach out to us.

            Best regards,
            Sales Team
            """
            message.attach(MIMEText(email_body, "plain"))

            # Send the email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:  # Use your email provider's SMTP settings
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, message.as_string())

            st.success("The sales proposal has been sent to the provided email!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please fill out all the required fields.")
