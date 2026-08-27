# Contributing to SOC Discord Bot

First off, thank you for considering contributing to this project! It’s people like you that make the open-source community such an amazing place to learn, inspire, and create.

Please take a moment to review this document before submitting any code or reporting issues.

---

## 🛠️ How Can I Contribute?

### 🐛 Reporting Bugs
If you found a bug, please use the **Bug Report Template** provided in the GitHub Issues section. Make sure to include system details and logs so we can fix it quickly.

### 💡 Suggesting Features
We love new ideas! If you want to suggest an improvement or a new feature (like a new Pterodactyl API feature or a new log parser):
1. Open an issue and use a clear title.
2. Describe the feature, why it is useful, and how it should work.

### 🧑‍💻 Submitting Code (Pull Requests)
Ready to write some code? Great! Please follow this workflow:

1. **Fork the Repository:** Create your own copy of this project on GitHub.
2. **Clone & Setup:** Clone your fork locally and set up your private testing environment. **Never test code on a live, production gameserver!**
3. **Create a Branch:** Create a branch with a descriptive name:
   * For features: `feature/your-feature-name`
   * For bug fixes: `bugfix/issue-number-or-name`
4. **Write Code:** Keep your code clean, readable, and well-commented.
5. **Commit Changes:** Write clear, concise commit messages (e.g., `fix: resolve auth.log parsing issue for failed root logins`).
6. **Push & Pull Request:** Push the branch to your fork and open a Pull Request (PR) against our `main` branch.

---

## 🔒 Security Policy

Since this bot has administrative access to a vServer (via SSH logs, Fail2Ban, and Pterodactyl APIs), **security is our highest priority**.

* **NO SECRETS:** Never commit actual API keys, Discord tokens, or passwords. Always use the `.env` file and make sure it is ignored by Git.
* **Input Validation:** Any user input from Discord commands must be strictly validated to prevent command injection or unauthorized access.
* **Reporting Vulnerabilities:** If you find a security vulnerability, **do not** open a public issue. Please contact the repository owner privately (see profile details).

---

## 📜 Code Style Guidelines

* Keep your code modular (e.g., separate parsers for Fail2Ban and Pterodactyl).
* Follow the standard style guide for the language used (e.g., **PEP 8** for Python or **ESLint** for JavaScript).
* Ensure that no new dependencies are added without explaining why they are necessary in your Pull Request.

Thank you again for your help!
