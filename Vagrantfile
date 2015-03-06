# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = 'ubuntu/trusty64'

  VM_IP = 200
  VM_NAME = "ceph#{VM_IP}"
  SUBNET='192.168.73'

  config.vm.hostname = VM_NAME

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network 'private_network', ip: "#{SUBNET}.#{VM_IP}"

  # Add a 1 GB drive to the VM to act as OSD drive
  config.vm.provider 'virtualbox' do |vbox|

    vbox.name = VM_NAME
    vbox.customize ['modifyvm', :id, '--memory', '512']

    1.times do |i|
      vbox.customize %W(createhd --filename disk-default-#{i} --size 1000)
      vbox.customize ['storageattach', :id, '--storagectl', 'SATAController', '--port', 3 + i, '--device', 0, '--type', 'hdd', '--medium', "disk-default-#{i}.vdi"]
    end

  end

  config.vm.provision 'ansible' do |ansible|
    ansible.playbook = 'ceph-ansible/site.yml'
    # Note: Can't do ranges like mon[0-2] in groups because
    # these aren't supported by Vagrant, see
    # https://github.com/mitchellh/vagrant/issues/3539
    ansible.groups = {
      'mons' => %w(default),
      'osds' => %w(default),
      'mdss' => %w(default),
      'rgws' => []
    }

    # In a production deployment, these should be secret
    ansible.extra_vars = {
      cephx: false, # disable cephx authentication

      ceph_dev: true, # use ceph development branch
      ceph_dev_branch: 'v0.92', # development branch you would like to use e.g: master, wip-hack

      fsid: '4a158d27-f750-41d5-9e7f-26ce4c9d2d45',
      monitor_secret: 'AQAWqilTCDh7CBAAawXt6kyTgLFCxSvJhTEmuw==',
      radosgw: 'false',
      mds: 'false',

      # Needed for single node
      common_single_host_mode: 'True',

      # Change to > 1 if you have more than one OSD
      pool_default_size: 1,

      # Has to reflect the same IP block in Vagrantfile
      cluster_network: "#{SUBNET}.0/24",
      public_network: "#{SUBNET}.0/24"
    }

    ansible.limit = 'all'
  end

  config.vm.provision 'shell', inline: 'sudo cp -r /etc/ceph /vagrant/etc/'

  # If true, then any SSH connections made will enable agent forwarding.
  # Default value: false
  config.ssh.forward_agent = true

end
