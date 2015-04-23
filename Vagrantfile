Vagrant.configure("2")  do |config|

  # base information
  config.vm.box = "scarlettpi-system"
  config.vm.box_url = "file:///Users/malcolm/scarlettpi-system.box"

  # name
  # CHANGME
  config.vm.hostname = "scarlettpi-system7"

  # networking
  #config.vm.network "private_network", ip: "192.168.5.10"
  config.vm.network :public_network
  config.vm.network "forwarded_port", guest: 80, host: 8180
  config.vm.network "forwarded_port", guest: 443, host: 4443
  config.vm.network "forwarded_port", guest: 19360, host: 1936

  config.ssh.username = "pi"
  config.ssh.host = "127.0.0.1"
  config.ssh.guest_port = "2222"
  config.ssh.private_key_path = "/Users/malcolm/.ssh/id_rsa"
  config.ssh.forward_agent = true
  config.ssh.forward_x11 = true
  #config.ssh.pty = true
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

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
