from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import random

def create_masked_pdf(output_filename, text_content):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 7)
    
    y = height - 50
    for line in text_content.split('\n'):
        if y < 30:
            c.showPage()
            c.setFont("Helvetica", 7)
            y = height - 50
        c.drawString(30, y, line)
        y -= 9
            
    c.save()

# Generate 60 realistic transactions (May + part of June 2026)
transactions_data = []
balance = 1000.00 # Starting balance

# Initial salary at the start of the month
transactions_data.append({
    'date': datetime(2026, 5, 1),
    'desc': "SALARY CREDIT",
    'amount': 5000.00,
    'is_credit': True
})
balance += 5000.00

# Generate 59 more transactions
for i in range(1, 60):
    # Determine date (spread over ~60 days)
    day = (i // 2) + 1
    month = 5 if day <= 31 else 6
    day_in_month = day if day <= 31 else day - 31
    date_obj = datetime(2026, month, day_in_month)
    
    # Check for mid-month salary
    if day == 15:
        amount = 2500.00
        desc = "MID-MONTH SALARY"
        is_credit = True
    else:
        # Daily expenses
        # Ensure expense does not exceed current balance
        max_expense = min(150.0, balance)
        amount = round(random.uniform(5.0, max_expense), 2)
        desc = random.choice(["Grocery", "Coffee", "Gas", "Utility", "Restaurant", "Transfer"])
        is_credit = False
        
    transactions_data.append({
        'date': date_obj,
        'desc': desc,
        'amount': amount,
        'is_credit': is_credit
    })

# Calculate running balance
transaction_lines = []
for t in transactions_data:
    if t['is_credit']:
        balance += t['amount']
        transaction_lines.append(f"{t['date'].strftime('%d/%m/%y')}    {t['desc'].ljust(25)} {t['amount']:.2f}+     {balance:.2f}")
    else:
        balance -= t['amount']
        transaction_lines.append(f"{t['date'].strftime('%d/%m/%y')}    {t['desc'].ljust(25)} {t['amount']:.2f}-     {balance:.2f}")

transaction_text = "\n".join(transaction_lines)

# Full redacted text content
masked_text = f"""
[NAME MASKED]
[ADDRESS MASKED]
ACCOUNT NUMBER: [ACCOUNT MASKED]
Statement Date: 31/05/26

URUSNIAGA AKAUN / ACCOUNT TRANSACTIONS
--------------------------------------
DATE        DESCRIPTION                      AMOUNT      BALANCE
01/05/26    BEGINNING BALANCE                            1000.00
{transaction_text}
--------------------------------------
ENDING BALANCE : {balance:.2f}
"""

create_masked_pdf("modules/bank_data/bank_statement_example.pdf", masked_text)
print("Masked PDF generated successfully with realistic salary pattern.")
