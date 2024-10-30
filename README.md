# Footie Analysis Tool

## Overview

When viewing league table results and player stats through usual means, it can be difficult to make future predictions based on these alone as they don't tell the full story. This tool was designed to help you make more informed decisions when it comes to betting and also beating your mates in FPL.

The tool is a Flask application developed in Python that ingests a variety of `.csv` files. The `.csv` files are used to create a number of graphics in matplotlib, detailing the best in a specific category. These categories include:

- Home/Away outcomes
- Both teams to score / clean sheets
- Corners
- League player-specific stats

The Python script is automatically deployed through a Docker container built using a CI/CD pipeline with GitHub Actions and hosted on an Azure or AWS VM.

Some challenges I faced when designing this include managing Docker caching and deployment consistency, ensuring the EC2 instance had internet access, and deploying the application with GitHub Actions for continuous delivery. Through perseverance, these challenges became manageable. In the future, more granular per-game statistics will be added, including shots, shots on target, free kicks conceded, half-time results, and player-specific stats for leagues beyond the Premier League.

## Installation Guide (AWS EC2 Instance)

### Prerequisites

To use the tool, a number of technologies need to be installed on a VM. This project was designed for use on Azure and AWS. The steps below outline the process for installing the app on an AWS EC2 instance.

1. **Create an AWS EC2 Instance**
   - Begin by creating an AWS account and then creating an EC2 instance. This can be done using the AWS portal, Terraform, AWS CLI, etc.
   - The `t2.micro` AMI image can be used on the free tier version of AWS.

2. **Create and Configure PEM Key**
   - Create a `.pem` key to access the VM using SSH. This can be done through the AWS portal by navigating to the EC2 page. Under **Network & Security**, click **Key Pairs** and create an RSA `.pem` file.
   - Save the `.pem` file in an easily accessible location.
   - Use the command `chmod 400 "your-file.pem"` on the CLI to ensure the key is not publicly viewable.

3. **Connect to Your VM**
   - To connect to your VM using VS Code, ensure the **Remote - SSH** extension is installed.
   - Use `CTRL + SHIFT + P` to open the SSH configuration file and add the following details:

     ```
     Host <Name of your choice>
       HostName <IP address of VM>
       User <username (usually ec2-user)>
       IdentityFile <path/to/your/pem/file>
     ```

   - Use `CTRL + SHIFT + P` again, select **Remote-SSH: Connect current window to Host**, and click on the host you configured.

4. **Install Dependencies on the VM**
   - Once connected, open the terminal and install Git. Configure your Git username and email. The commands vary depending on your OS and distribution.
   - Install Docker. The method will vary based on your OS and distribution. Use `sudo service docker start` to ensure Docker is running on your VM.

5. **Clone the Repository and Set Up Git**
   - Use the command `git clone https://github.com/emoore0/football-analysis.git`.
   - On your GitHub account, create a new repository and add your own remote:
     ```
     git remote add origin https://github.com/yourusername/your-new-repo.git
     ```
   - Push to your new repository using `git push -u origin main`.

6. **Configure GitHub Secrets**
   - In the settings page of your GitHub repository, navigate to **Secrets and variables** under **Actions**. Add the following secrets:
     - `AWS_EC2_HOST` - IP address of your VM
     - `AWS_EC2_SSH_KEY` - Contents of your PEM file
     - `DOCKER_PASSWORD` - Docker personal access token with Read, Write, Delete access
     - `DOCKER_USERNAME` - Your Docker username

7. **Log In to Docker and Build the Image**
   - Use the command `docker login` and enter your Docker email and password.
   - Build an image with the command:
     ```
     docker build -t your-username/football-app:latest .
     ```

8. **Check Docker Logs and Verify Deployment**
   - Use `sudo docker ps -a` to get the container ID, then view logs with:
     ```
     sudo docker logs <first 3 letters of container id>
     ```
   - Click on the IP address it's running on to view the contents and graphs and ensure everything is working.

9. **Push Changes and Update GitHub Actions Workflow**
   - Make changes to the Python script or commands as needed and push them to GitHub.
   - Change the `deploy.yml` file to match your branch of choice, commit, and push. Once GitHub Actions completes, your VM should be accessible with its IP address.

   If you encounter an "Internal Server Error," use `docker logs` on your container to troubleshoot.

10. **Troubleshoot Docker Caching**
    - On a `t2.micro` VM, there may be issues with Docker caching and deployment consistency. If needed, free up space with:
      ```
      sudo docker system prune -f
      ```
