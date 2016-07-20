
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"

  # Configure the network to forward port 8000 to the host
  config.vm.network :forwarded_port, guest: 5000, host: 5000

  # Update and upgrade ubuntu
  config.vm.provision "shell", inline: "apt-get update && apt-get upgrade -y"

  # Install the necessary dependencies for development
  config.vm.provision "shell", inline: "apt-get install python-pip libpq-dev python-dev libffi-dev -y"

  # Install heroku toolkit
  config.vm.provision "shell", inline: "wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh"
  config.vm.provision "shell", inline: "heroku --version", privileged: false

  # Run pip install for Python requirements
  config.vm.provision "shell", inline: "pip install -r /vagrant/requirements.txt"

end
