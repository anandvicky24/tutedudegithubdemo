Here are the steps to create an SSH key in Windows and add it to GitHub:

1. Open PowerShell as Administrator and run:

Replace your_email@example.com with your actual email.

2. When prompted for file location, press Enter to accept the default (C:\Users\YourUsername\.ssh\id_ed25519).

3. When prompted for passphrase, press Enter twice (or enter a secure passphrase).

4. Display your public key by running:

5. Copy the entire output (starts with ssh-ed25519).

6. Add to GitHub:

Go to https://github.com/settings/keys
Click "New SSH key"
Paste your public key
Click "Add SSH key"
7. Verify the connection:

You should see: Hi username! You've successfully authenticated...