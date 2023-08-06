
# NOTE: This address must be verified with Amazon SES.
SENDER = "Sender <no-reply@sender.com>"

# AWS Region you're using for Amazon SES.
AWS_REGION = "us-east-1"

# The character encoding for the email.
CHARSET = "UTF-8"

# This variable should be passed in from the invoker.
# NOTE: If your account is still in the sandbox, this address must be verified.
DEFAULT_RECIPIENT = "default@recipient.com"

# The default subject line for the email.
DEFAULT_SUBJECT = "Default email subject"

# The default email body for recipients with non-HTML email clients.
DEFAULT_BODY_TEXT = ("Default email body, non HTML version. No one should ever get this email.")
            
# The default HTML body of the email.
DEFAULT_BODY_HTML = """<html>
<head></head>
<body>
  <h1>Default email body</h1>
  <p>
    <a href='https://default.com/'>Default</a> test email, HTML version. No one should ever get this email.
  </p>
</body>
</html>
            """      