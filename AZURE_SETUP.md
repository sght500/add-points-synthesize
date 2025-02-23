# Setting Up Microsoft Azure Speech Service (Free Tier)

## Introduction

This guide walks you through **creating a free Microsoft Azure account** and **deploying a free-tier Speech Service instance** to use with our project.

---

## Step 1: Create a Free Microsoft Azure Account

1. Go to [Azure Free Account](https://azure.microsoft.com/free/).
2. Click **Start Free** and sign in with your Microsoft account.
3. Complete the required details and **verify your identity** (a credit card may be required, but you won’t be charged for free-tier usage).
4. Once the account is created, go to the **Azure Portal**: [https://portal.azure.com](https://portal.azure.com).

---

## Step 2: Create a Free Speech Service Instance

1. In the **Azure Portal**, search for **Speech Services** in the top search bar.
2. Click **Create** and fill in the following details:
   - **Subscription**: Select the free-tier subscription.
   - **Resource Group**: Click **Create new** and enter a name (e.g., `speech-resources`).
   - **Region**: Choose the region closest to you.
   - **Pricing Tier**: Select the **Free Tier (F0)**.
   - **Name**: Enter a unique name for your Speech Service instance.
3. Click **Review + Create** and then **Create**.
4. Wait for deployment to complete, then click **Go to Resource**.

---

## Step 3: Retrieve Your Subscription Key and Region

1. In your **Speech Service resource**, navigate to **Keys and Endpoint**.
2. Copy **Key 1** – this is your `SPEECH_KEY`.
3. Copy the **Region** (e.g., `westus` or `eastus`) – this is your `SPEECH_REGION`.

---

## Step 4: Set Up Environment Variables

To use the Speech Service in your project, set the following environment variables:

### **On Windows (PowerShell):**

```powershell
setx SPEECH_KEY your_subscription_key
setx SPEECH_REGION your_region
```

### **On macOS/Linux:**

```bash
export SPEECH_KEY=your_subscription_key
export SPEECH_REGION=your_region
```

This ensures the application can access your Speech Service.

---

## Bonus: Get API Access by Contributing!

If you’d like **free access** to my personal API Key (`SPEECH_KEY` and `SPEECH_REGION`), you can contribute to one of my open-source projects!

### How it works:

1. Visit my [GitHub Issues](https://github.com/sght500?tab=repositories).
2. Pick an **open issue** from any of my repositories.
3. Solve it and submit a **Pull Request (PR)**.
4. Once approved, I’ll send you **temporary access** to my API Key!

This is a great way to **learn, contribute, and get premium API access for free**!

---

### Need Help?

If you run into issues, feel free to ask in the project’s **GitHub Discussions** or open an issue!

Happy coding! 🚀
