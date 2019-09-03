nginx [engine x] is an HTTP and reverse proxy server, a mail proxy server, and a generic TCP/UDP proxy server, originally written by Igor Sysoev.
We use nginx to handle the request from user to our website.

1. Install nginx 

`sudo apt-get -y install nginx`
`sudo service nginx start`

2. Default configuration for nginx. 

Nginx by default come with a configuration to open a default page. After step 1, if the nginx is installed and the service is started, you could type in your favorate browser the IP Address (or domain name with name solution configured for the IP Address) of your server, it will show a default page. However, what we want is when user type in our IP Address (or domain), they were naviagated to our website. To achieve this, proceed to step 3

3. Configure our site for nginx.

Open a new file at `/etc/nginx/sites-available/` with your favorate editor

Reference to `euclid.conf` for the configuration. Replace all the name / directories with yours. 

Also, you should create the non existing folders, such as `log`, `media`, using `mkdir` at the location you set in the configuration file.

4. Enable the site.
Now we had the configuration at the `sites-available` folder. However, nginx will only respond to the configurations placed at `sites-enabled` folder. 

To achieve this, (*simple*) copy the configuration file to `sites-enabled`, or (*recommended*) create a symbolic link for the configuration file in `sites-available` to `sites-enabled` by using the following command.

`sudo ln -s /etc/nginx/sites-available/<configration> /etc/nginx/sites-enabled/<configration>`

And restart the service. 

`sudo service nginx restart`

Remember, everytime you edit the configuration file, the new file should be either copied, or symbolically linked to `sites-enabled`, And ther service should be restarted.