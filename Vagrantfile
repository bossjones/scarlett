Vagrant.configure("2")  do |config|

  # base information
  config.vm.box = "scarlettpi-system"
  config.vm.box_url = "file:///Users/malcolm/Downloads/scarlett_9_27_2015.box"

  # name
  # CHANGME
  config.vm.hostname = "scarlettpi-system7"
  config.vm.boot_timeout = 400

  # networking
  config.vm.network "public_network", :bridge => 'en0: Wi-Fi (AirPort)'
  config.vm.network "forwarded_port", guest: 19360, host: 1936
  config.vm.network "forwarded_port", guest: 139, host: 1139
  config.vm.network "forwarded_port", guest: 8081, host: 8881

  config.ssh.username = "pi"
  config.ssh.host = "127.0.0.1"
  config.ssh.guest_port = "2222"
  config.ssh.private_key_path = "/Users/malcolm/.ssh/id_rsa"
  config.ssh.forward_agent = true
  config.ssh.forward_x11 = true
  #config.ssh.pty = true
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

  config.vm.provision "shell", path: "./bootstrap/start_anaconda.sh"

  config.vm.provider :virtualbox do |vb|
    # Don't boot with headless mode
    vb.gui = true

    # user modifiable memory/cpu settings
    vb.memory = 1024
    vb.cpus = 1

    # use host dns resolver
    # vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

end
