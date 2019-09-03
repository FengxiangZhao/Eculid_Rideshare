# Setting up the server in EC2 Ubuntu


## Prerequisites

### Infrastructure

- EC2 Instance

### Software

Run the following script on the shell to get the required packages

```
# Update the whole environment
sudo apt-get -y update
sudo apt-get -y upgrade

# Install software
sudo apt-get -y install python3-setuptools python3-dev build-essential unzip python3-pip virtualenv gunicorn nginx supervisor
sudo pip3 install --upgrade pip3
```

## Setting up a site-specific account

It is not recommended to use the default user of EC2 to use a website for safety concerns. 

- Setting up the group: 

`sudo groupadd --system websites`

- Adding a site-specific user to the group

`sudo useradd --system --gid websites --shell /bin/bash --home /websites/euclid euclid`

- Make the HOME for the account

`sudo mkdir -p /websites/euclid`

## Obtain The Project Body

### FTP

Use your favorite FTP software to upload the whole Django project to the EC2 instance. Remember to exclude the database (if you are using sqlite, exclude `db.sqlite`) or temporary folders such as `__pychache__` or `migrations`.

### Git Repository (Recommended)

If you are using a public git repository, you could directly pull from the git url. However, if you are in a private one, before you pull, you must select an method of authentication to access the repository. The following section covers how to use SSH authentication.

#### Private Git Repository

Assuming we are using the default user for EC2 Ubuntu, and you are hosting your private git repository in the popular online repositories (Github, GitLab), and the repository is accessible using the typical SSH connection.

1. Switch to the User you just created.

`sudo su - euclid`

2. Generate a SSH key for the user

`ssh-keygen -o -t rsa -C "<your own identifiers for this key>" -b 4096`

3. Obtain the key

Assume that you save to the default location `~/.ssh/id_rsa.pub`

`cat ~/.ssh/id_rsa.pub`

Otherwise,

`cat <key location>`

4. Add the key to your Git account

Generally, if you are using Github or Gitlab, go to settings for you account, find SSH keys, and follow the directions there.

## Setting Up the Environment 

### Django Project Dependencies

It is necessary to use virtual env so that the website environment is separate from the server environment.

1. Create a virtual environment in the project folder and activate

`virtualenv --python=python3 --always-copy <foldername>`

`source <foldername>/bin/activate`

2. Install necesary packages

It is laborious to type in all the required packages in `pip install`, so before you proceed, export the dependencies in your development environemt by using `pip freeze > requirement.txt`, and upload the file to the EC2 instance. 

Install the dependencies under the virtual env using
`pip install -r <path to requirement.txt>`

3. Check installation and migrate

Use `python manage.py check` and make migrations to the django project.

### Gunicorn

Follow the instructions in Gunicorn folder