Supervisor is a client/server system that allows its users to control a number of processes on UNIX-like operating systems.
We use Supervisor to control the service of our website.

1. Install supervisor
` sudo apt-get -y install supervisor `

2. Configure the service of your website

Open a new file at `/etc/supervisor/conf.d/` for your configuration.

In our case, the start command should refernce to the locaiton of `gunicorn_start.sh`

3. Validate and execute the service using supervisor

`sudo supervisorctl reread` 

Output should show the name of the service to and status should be available

`sudo supervisorctl update` 

If the configuration file is correct, your service should be added to the group. 
Otherwise you should be getting some error message from supervisor.

4(and later). Use these conmmand to control your service. The parameter shows what should be done. 
```
sudo supervisorctl status <configuration>
sudo supervisorctl start <configuration>
sudo supervisorctl stop <configuration>
sudo supervisorctl restart <configuration>
```
