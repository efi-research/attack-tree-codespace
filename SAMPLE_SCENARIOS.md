# Sample Attack Scenarios

Use these scenarios to test and demonstrate the Attack Tree Generator. Simply copy the title and description into the web interface.

---

## 1. E-Commerce Platform Breach

**Title:** E-Commerce Customer Data Theft

**Description:** An attacker wants to steal customer credit card information and personal data from an e-commerce platform. The platform uses HTTPS, stores payment data in a PCI-DSS compliant database, has a web application firewall, implements rate limiting, and uses tokenization for credit card processing. The system has admin panels, customer-facing web applications, and integrates with third-party payment processors.

---

## 2. Smart Home IoT Attack

**Title:** Smart Home Device Takeover

**Description:** An attacker aims to gain control of smart home devices including security cameras, door locks, and thermostats. The devices communicate via WiFi and a central hub, use cloud services for remote access, have mobile apps for control, and implement firmware update mechanisms. Some devices use default credentials and have known vulnerabilities.

---

## 3. Corporate Email Compromise

**Title:** Business Email Compromise Attack

**Description:** An attacker wants to compromise executive email accounts to perform wire fraud and steal sensitive business information. The organization uses Office 365 with multi-factor authentication, has email filtering and anti-phishing tools, conducts security awareness training, and has policies for financial transactions. Executives frequently travel and access email from various locations.

---

## 4. Healthcare Records Breach

**Title:** Electronic Health Records Theft

**Description:** An attacker seeks to access and exfiltrate patient medical records from a hospital system. The hospital uses Electronic Health Records (EHR) systems with role-based access control, encrypts data at rest and in transit, has audit logging, complies with HIPAA regulations, and has multiple access points including doctor workstations, nurse stations, and administrative terminals.

---

## 5. Banking Mobile App Attack

**Title:** Mobile Banking Application Compromise

**Description:** An attacker wants to steal money from user accounts through a mobile banking application. The app uses certificate pinning, implements biometric authentication, has transaction limits, uses device fingerprinting, includes fraud detection systems, and communicates with backend services through encrypted APIs. Users can transfer money, pay bills, and view account information.

---

## 6. Cloud Infrastructure Takeover

**Title:** AWS Cloud Infrastructure Compromise

**Description:** An attacker aims to gain control of an organization's AWS cloud infrastructure to steal data, mine cryptocurrency, or launch attacks. The infrastructure includes EC2 instances, S3 buckets, RDS databases, Lambda functions, and uses IAM for access control. Some services are publicly accessible, and the organization uses multiple AWS accounts with varying security configurations.

---

## 7. Social Media Account Hijacking

**Title:** High-Profile Social Media Account Takeover

**Description:** An attacker wants to take control of a celebrity or corporate social media account to spread misinformation, scam followers, or damage reputation. The account has two-factor authentication enabled, uses a strong password, is accessed from multiple devices and locations, has recovery email and phone number configured, and the platform has account protection features and anomaly detection.

---

## 8. Supply Chain Software Attack

**Title:** Software Supply Chain Compromise

**Description:** An attacker seeks to inject malicious code into a widely-used open-source software library to compromise downstream applications. The library is hosted on GitHub, uses automated CI/CD pipelines, has multiple maintainers with varying security practices, is distributed via npm/PyPI, and is used by thousands of applications. The attack could target the build process, dependencies, or maintainer accounts.

---

## 9. Physical Data Center Breach

**Title:** Data Center Physical Access Attack

**Description:** An attacker wants to gain physical access to a data center to install hardware implants, steal hard drives, or cause service disruption. The facility has perimeter fencing, security guards, badge access systems, biometric scanners, video surveillance, mantrap entrances, and is located in a secure building. The data center houses critical servers and network equipment.

---

## 10. Ransomware Deployment

**Title:** Enterprise Ransomware Attack

**Description:** An attacker aims to deploy ransomware across a corporate network to encrypt all business data and demand payment. The network has endpoint protection, network segmentation, backup systems, email filtering, user access controls, patch management processes, and security monitoring. The organization has remote workers, on-premise servers, and cloud services.

---

## 11. API Security Breach

**Title:** RESTful API Exploitation

**Description:** An attacker wants to exploit vulnerabilities in a company's REST API to access unauthorized data or perform privilege escalation. The API uses OAuth 2.0 authentication, has rate limiting, implements input validation, uses HTTPS, has API keys for different access levels, and serves both web and mobile applications. Some endpoints are public while others require authentication.

---

## 12. Cryptocurrency Exchange Hack

**Title:** Cryptocurrency Exchange Wallet Theft

**Description:** An attacker seeks to steal cryptocurrency from a digital currency exchange's hot and cold wallets. The exchange uses multi-signature wallets, implements withdrawal limits and delays, has KYC/AML procedures, uses hardware security modules, maintains cold storage for majority of funds, and has real-time transaction monitoring. The platform handles millions in daily trading volume.

---

## 13. Industrial Control System Attack

**Title:** SCADA System Sabotage

**Description:** An attacker wants to disrupt operations of an industrial facility by compromising SCADA/ICS systems controlling manufacturing processes. The systems use proprietary protocols, have air-gapped networks, implement physical security controls, use legacy operating systems with limited patching, have HMI interfaces for operators, and control critical infrastructure like water treatment, power generation, or chemical processing.

---

## 14. University Research Data Theft

**Title:** Academic Research IP Theft

**Description:** An attacker aims to steal valuable research data and intellectual property from a university research department. The university has network access controls, uses VPN for remote access, has shared computing resources, stores data on network drives and cloud services, has student and faculty accounts with varying privileges, and the research involves sensitive data that could be valuable to competitors or nation-states.

---

## 15. Autonomous Vehicle Hijacking

**Title:** Self-Driving Car Remote Control

**Description:** An attacker wants to remotely take control of autonomous vehicles to cause accidents, kidnapping, or mass disruption. The vehicles use multiple sensors (cameras, lidar, radar), communicate with cloud services for updates and navigation, have over-the-air update mechanisms, use AI for decision-making, connect to mobile apps, and implement various safety systems. The attack could target the vehicle directly or the supporting infrastructure.

---

## Tips for Using These Scenarios

1. **Start Simple**: Try scenarios 1-3 first as they're more straightforward
2. **Experiment**: Modify the descriptions to add or remove security controls
3. **Compare Results**: Generate the same scenario multiple times to see variations
4. **Mix and Match**: Combine elements from different scenarios
5. **Create Your Own**: Use these as templates for your specific use cases

## Quick Test (Simple)

**Title:** Password Reset Attack

**Description:** An attacker wants to gain access to a user account by exploiting the password reset functionality. The system sends reset links via email and asks security questions.

---

*Press `Ctrl+Shift+S` in the web interface to auto-fill a sample scenario for quick testing!*
