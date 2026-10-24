import pandas as pd

# Document schema padi column list
data = [
    {
        "message_id": "MSG_001",
        "channel": "email",
        "subject_or_title": "Urgent: Update your direct deposit information",
        "body_text": "Your payroll access is suspended. Please verify your bank details immediately at hxxp://payroll-update[.]com.",
        "sanitized_url_features": "hxxp,lookalike_domain",
        "sender_domain_type": "lookalike",
        "label": "phishing",
        "campaign_group": "payroll_urgent_scam",
        "collected_date": "2026-10-18"
    },
    {
        "message_id": "MSG_002",
        "channel": "email",
        "subject_or_title": "Monthly Payroll Summary",
        "body_text": "Your payslip for this month is ready for download in the internal HR portal.",
        "sanitized_url_features": "none",
        "sender_domain_type": "internal",
        "label": "legitimate",
        "campaign_group": "internal_hr_payroll",
        "collected_date": "2026-10-18"
    },
    {
        "message_id": "MSG_003",
        "channel": "sms",
        "subject_or_title": "Package delivery notification",
        "body_text": "Final notice: Your shipment is on hold due to missing fee. Visit hxxp://track-fee[.]cc/pay now.",
        "sanitized_url_features": "hxxp,shortener",
        "sender_domain_type": "unknown",
        "label": "phishing",
        "campaign_group": "delivery_scam",
        "collected_date": "2026-10-18"
    },
    {
        "message_id": "MSG_004",
        "channel": "email",
        "subject_or_title": "Password reset verification code",
        "body_text": "Your single-use password reset code is 482910. If you did not request this, ignore this email.",
        "sanitized_url_features": "none",
        "sender_domain_type": "internal",
        "label": "legitimate",
        "campaign_group": "auth_password_reset",
        "collected_date": "2026-10-18"
    }
]

df = pd.DataFrame(data)
df.to_csv("dataset.csv", index=False)
print("dataset.csv successfully created with correct schema!")