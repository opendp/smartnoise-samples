
sudo curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

#Ubuntu 18.04
sudo curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list


sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install --yes msodbcsql17
sudo ACCEPT_EULA=Y apt-get install --yes mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get install --yes unixodbc-dev