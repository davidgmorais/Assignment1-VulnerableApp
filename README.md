# Assignment1-VulnerableApp
Assignment in the scope of the course of Analysis and Exploration of Vulnerabilities of the Cybersecurity Masters degree, and it was focus on the existence of vulnerabilities in software projects, and their avoidance

## Description
The main purpose of the application is a web store, where users, after creating an account, are able to buy and sell seconf hand furniture online. There are bot a vulnerable application as well as a fixed version of the same application and the project was developed in Python using Flask and MySQL, being ready for deployment using the `docker-compose.yml` file in each directory. Furthermore, the scripts used for the anlaysis, some print screens and the report documenting the process are all present in the `/analysis` directory.

## Vulnerabilities
The present vulnerabilities are as follows:
- CWE-521: Weak Password Requirements
- CWE-287: Improper Authentication
- CWE-89: SQL Injection
- CWE-22: Path Transversal
- CWE-434: Unrestricted Upload of File with Dangerous Type
- CWE-79: Cross-site Scripting

## Team
[David Morais, 93147](https://github.com/davidgmorais)	

[Gerson Catito, 105428](https://github.com/GersonCatito)
