# Creating a Google Service Account and Sharing a Folder

This guide will walk you through the process of creating a Google service account, exporting its credentials, finding its email address, and sharing a Google Drive folder with that email address.

## 1. Creating a Service Account

1. **Go to the Google Cloud Console:** Open your web browser and navigate to the [Google Cloud Console](https://console.cloud.google.com/).
2. **Create or Select a Project:** If you don't have a project, create one. Otherwise, select the existing project you want to use.
3. **Go to Service Accounts:** In the navigation menu, go to **IAM & Admin** > **Service Accounts**.
4. **Create a Service Account:** Click **Create Service Account**.
5. **Enter Details:** Provide a **Service Account Name** and an optional **Service Account ID**.
6. **Create Key:** Click **Create and continue**.
7. **Create a Key:**
    * Select **JSON** as the **Key type**.
    * Click **Create**. This will download a JSON file containing your service account credentials. **Store this file securely, as it will be the only way to access this service account.**

## 2. Finding the Service Account Email Address

1. **Go to the Service Account Details:** In the Service Accounts list, click on the service account you just created.
2. **Find the Email Address:** The service account's email address is displayed under the service account name.

## 3. Sharing a Folder with the Service Account

1. **Open the Folder:** In Google Drive, open the folder you want to share.
2. **Click "Share":** Click the **Share** button (looks like a person with a plus sign).
3. **Add Collaborators:**
    * In the "People" field, enter the **service account's email address**.
    * Choose the appropriate **permission level** (e.g., Viewer, Editor, Commenter).
    * Click **Send**.

**Note:**

* The service account will now have access to the shared folder based on the permissions you granted.
* You can use the downloaded JSON credentials to authenticate your applications with Google services using the service account.

**Additional Tips:**

* For enhanced security, consider creating a separate service account for each application or use a service account key that is rotated regularly.
* Be mindful of the permissions granted to the service account. Only grant the necessary permissions to minimize the risk of unauthorized access.

By following these steps, you can successfully create a Google service account, obtain its credentials, and share a folder with it, enabling your applications to interact with Google services securely and efficiently.
