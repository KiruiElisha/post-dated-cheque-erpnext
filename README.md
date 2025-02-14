## Post Dated Cheque App for ERPNext

The **Post Dated Cheque (PDC) App** integrates seamlessly with ERPNext to streamline the management of post dated cheques. This app automates the creation of Payment Entries upon cheque submission and provides detailed cheque statement reports—including cheque numbers, bank details, and amounts—that can be emailed directly to stakeholders.

---

## Overview

The Post Dated Cheque App is designed to simplify cheque management in ERPNext. Key functionalities include:

- **Automated Payment Entry Creation:** Automatically generates a Payment Entry when a cheque is submitted.
- **Cheque Statement Reporting:** Provides detailed reports with cheque numbers, bank account information, amounts, and more.
- **Email Reporting:** Allows you to send cheque statement reports via email for improved communication and record-keeping.
- **Seamless ERPNext Integration:** Works natively within ERPNext, ensuring data consistency and streamlined financial operations.

---

## Key Features

- **Post Dated Cheque Management:**  
  Create, edit, and track post dated cheques directly within ERPNext.

- **Automated Payment Entry Generation:**  
  On cheque submission, a corresponding Payment Entry is automatically created, reducing manual data entry.

- **Detailed Cheque Statement Report:**  
  Generate comprehensive reports that include cheque numbers, bank account details, amounts, and transaction information.

- **Email Notifications and Reporting:**  
  Easily email the generated cheque statement reports to stakeholders.

- **Intuitive User Interface:**  
  Leverages ERPNext’s familiar interface for a smooth and efficient user experience.

---

## Installation

### Prerequisites

- **ERPNext:** Ensure that ERPNext is installed and configured.
- **Frappe Framework:** The app is built on the Frappe framework.

### Installation Steps

1. **Clone or Download the App:**

   ```bash
   bench get-app https://github.com/AQIQ786/post_dated_cheque_app
   ```

2. **Install the App on Your Site:**

   ```bash
   bench --site <site-name> install-app post_dated_cheque_app
   ```

3. **Restart Bench:**

   ```bash
   bench restart
   ```

---

## Getting Started

### Creating a Post Dated Cheque

1. **Access the Module:**  
   Navigate to the Post Dated Cheque module via ERPNext’s desk or search using the awesome bar.

2. **Enter Cheque Details:**  
   Fill in the required details such as cheque number, bank account, amount, and other pertinent information.

3. **Submit the Cheque:**  
   When the cheque is submitted, a corresponding Payment Entry is automatically generated.

   ![Cheque Submission Screenshot](path/to/cheque_submission_image.png)

### Viewing Cheque Statement Reports

- **Access the Report:**  
  Go to the Reports section within the Post Dated Cheque module to view detailed cheque statements.

- **Report Details:**  
  The report includes information such as cheque numbers, bank account details, amounts, and more.

- **Email the Report:**  
  Use the built-in email functionality to send the cheque statement report to designated recipients.

  ![Cheque Statement Report Screenshot](path/to/cheque_statement_report_image.png)

---

## Email Notifications

Ensure your ERPNext email settings are correctly configured to fully utilize the app's email functionality. This enables automated sending of cheque statement reports and other notifications.

---

## Additional Configuration

- **Cheque Statement Customization:**  
  Modify report templates as needed to match your business requirements.

- **Integration Settings:**  
  Update settings such as default bank accounts and email templates within ERPNext.

- **Statement Details:**  
  The app also provides a detailed statement report which includes cheque numbers and related details. This report can be easily shared via email.

  ![Statement Detail Screenshot](path/to/statement_detail_image.png)

---

## Contributing

Contributions are welcome! If you have suggestions, improvements, or bug fixes, please fork the repository and submit a pull request.

---

## License

This app is open-source and available under the [MIT License](LICENSE).

---

## Support

For issues, questions, or further assistance, please open an issue on the [GitHub repository](https://github.com/yourusername/post_dated_cheque_app/issues) or contact the maintainers.
