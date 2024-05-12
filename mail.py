import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
from datetime import datetime
import json

def send_email():
    # Email configuration
    config = json.load(open('config.json', 'r'))
    sender_email = config['email']['s_id']
    receiver_email = config['email']['r_id']
    password = config['email']['password']

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('Failed to send the original mail')
    msg['Subject'] = "Daily Report"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Create the body of the message (a plain-text and an HTML version).
    text = """
    Dear [Recipient's Name],

    I hope this email finds you well.

    Please find below your daily report for [Date]:

    1. Sales Performance:
    - Total Sales: $XXXX
    - Top-selling Product: [Product Name]
    - Revenue Trend: [Brief Description]

    2. Website Analytics:
    - Total Visitors: XXXX
    - Pageviews: XXXX
    - Top Traffic Source: [Source]

    3. Project Updates:
    - Project A: [Brief update]
    - Project B: [Brief update]

    4. To-Do List:
    - Task 1: [Description]
    - Task 2: [Description]
    - Task 3: [Description]

    Please let me know if you need any further information or assistance.

    Best regards,
    [Your Name]
    """

    html = """\
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Daily Report</title>
    </head>
    <body>
        <p>Dear [Recipient's Name],</p>
        <p>I hope this email finds you well.</p>
        <p>Please find below your daily report for [Date]:</p>
        
        <ol>
            <li>
                <strong>Sales Performance:</strong>
                <ul>
                    <li>Total Sales: $XXXX</li>
                    <li>Top-selling Product: [Product Name]</li>
                    <li>Revenue Trend: [Brief Description]</li>
                </ul>
            </li>
            <li>
                <strong>Website Analytics:</strong>
                <ul>
                    <li>Total Visitors: XXXX</li>
                    <li>Pageviews: XXXX</li>
                    <li>Top Traffic Source: [Source]</li>
                </ul>
            </li>
            <li>
                <strong>Project Updates:</strong>
                <ul>
                    <li>Project A: [Brief update]</li>
                    <li>Project B: [Brief update]</li>
                </ul>
            </li>
            <li>
                <strong>To-Do List:</strong>
                <ul>
                    <li>Task 1: [Description]</li>
                    <li>Task 2: [Description]</li>
                    <li>Task 3: [Description]</li>
                </ul>
            </li>
        </ol>
        
        <p>Please let me know if you need any further information or assistance.</p>
        <p>Best regards,<br>[Your Name]</p>
    </body>
    </html>
    """

    # Attach both plain-text and HTML versions
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Email sent successfully at", datetime.now())

# Schedule the email to be sent daily at a specific time
schedule.every().day.at("01:47").do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)
