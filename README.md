# Footie Analysis Tool

## When viewing league table results and player stats through usual means it can be difficult to make future predictions based on these alone as they don't tell the full story. This tool was designed to help you make more informed decisions when it comes to betting and also beating your mates in FPL. 

### The tool is a Flask application developed in Python that ingests a variety of .csv files. The .csv files are used to create a number of graphics in matplotlib detailing in order the best in a certain catergory. These catergories include: 

 -Home/Away outcomes 
 -Both team to score clean sheets
 -Corners
 -League player specific stats

 The python scipt is automatically deployed through a Docker container built using a CI/CD pipeline using Github Actions that is ultimately hosted on an Azure or AWS VM. 

 Some challenges I faced when designing this include managing Docker caching and deployment consistency, ensuring the EC2 instance had internet access and deploying the application with github actions for continuos delivery but these all became manageable through perseverance. In the future, more granular per game statistics will be included to already existing functions and new ones including shots, shots on target, free kicks conceded, half time results and player specific stats for leagues other than the PL.

## To use the tool, a number of technologies need to be installed on a VM. This project was designed for use on Azure and AWS. I will outline the process for installing a the app on an AWS EC2 instance below:

To begin create a an EC2 instance. This can be done in a number of ways including the AWS portal, Terraform, AWS CLI etc. Next create a .PEM that will enable you to have access to the VM and store it in a safe location.