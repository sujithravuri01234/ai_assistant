"""
escalation_agent.py
-------------------
Handles queries that need human intervention:
  - Negative sentiment
  - Unknown department

Stretch Goal 2: Collects user details (name, phone, email) and
returns a confirmation message. Optionally sends an email via SendGrid.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def escalate_to_human(
    query: str,
    reason: str,
    user_name: str = None,
    user_email: str = None,
    user_phone: str = None
) -> dict:
    """
    Handle escalation to a human support agent.
    
    Args:
        query: The user's original query
        reason: Reason for escalation ('negative_sentiment' or 'unknown_department')
        user_name: Collected user name (optional — from form)
        user_email: Collected user email (optional — from form)
        user_phone: Collected user phone (optional — from form)
    
    Returns:
        dict with 'message' (shown to user) and 'requires_form' (bool)
    """

    # If we don't have user details, ask for them 
    if not all([user_name, user_email, user_phone]):
        return {
            "message": (
                "I understand you need assistance that requires a human touch. "
                "Please provide your contact details so our support team can reach out to you."
            ),
            "requires_form": True,
            "reason": reason
        }

    # We have user details — confirm and optionally send email
    _send_escalation_notification(query, user_name, user_email, user_phone, reason)

    if reason == "negative_sentiment":
        message = (
            f"Hello {user_name}, we sincerely apologize for your experience. "
            f"Your concern has been escalated to our senior support team. "
            f"A dedicated agent will contact you at {user_phone} or {user_email} within the next 2 hours. "
            f"Your ticket reference is #SUN-{abs(hash(user_email + query)) % 100000:05d}. "
            f"Thank you for your patience!"
        )
    else:
        message = (
            f"Hello {user_name}, thank you for reaching out to Sujith. "
            f"Your query has been received and assigned to our support team. "
            f"A support agent will contact you at {user_phone} or {user_email} within 24 hours. "
            f"Your ticket reference is #SUN-{abs(hash(user_email + query)) % 100000:05d}."
        )

    return {
        "message": message,
        "requires_form": False,
        "ticket_id": f"#SUN-{abs(hash(user_email + query)) % 100000:05d}",
        "user_name": user_name,
        "user_email": user_email,
        "user_phone": user_phone
    }


def _send_escalation_notification(query, name, email, phone, reason):
    """
    Optionally send an email notification using SendGrid.
    Fails gracefully if SendGrid key is not configured.
    """
    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    support_email = os.getenv("SUPPORT_EMAIL", "support@sujith.com")

    if not sendgrid_key or sendgrid_key == "your_sendgrid_api_key_here":
        print(f"[Escalation] Email notification skipped (SendGrid not configured)")
        print(f"  → Would notify {support_email} about escalation from {name} ({email})")
        return

    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail

        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_key)
        message = Mail(
            from_email=support_email,
            to_emails=support_email,
            subject=f"[Sujith Escalation] {reason.replace('_', ' ').title()} — {name}",
            html_content=f"""
            <h2>New Escalation Request</h2>
            <p><b>Reason:</b> {reason}</p>
            <p><b>Customer Name:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Phone:</b> {phone}</p>
            <p><b>Query:</b> {query}</p>
            """
        )
        sg.send(message)
        print(f"[Escalation] Email sent to {support_email}")
    except Exception as e:
        print(f"[Escalation] Email notification failed: {e}")


if __name__ == "__main__":
    # Test without form
    result = escalate_to_human(
        query="This is absolutely terrible! My order never came!",
        reason="negative_sentiment"
    )
    print("Without user details:", result)
    print()

    # Test with form details
    result = escalate_to_human(
        query="This is absolutely terrible! My order never came!",
        reason="negative_sentiment",
        user_name="Sujitha",
        user_email="sujitha@example.com",
        user_phone="+91-9876543210"
    )
    print("With user details:", result)
