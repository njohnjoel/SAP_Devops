import subprocess
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVER_CONFIG = {
    'appserver': {
        'hostname': 'appserver01.lab',
        'ip': '172.16.1.71',
        'netmask': '255.255.255.0',
        'gateway': '172.16.1.1',
        'interface': 'eth0'
    },
    's4hanadb': {
        'hostname': 's4hanadb01.lab',
        'ip': '172.16.1.72',
        'netmask': '255.255.255.0',
        'gateway': '172.16.1.1',
        'interface': 'eth0'
    },
    'devops': {
        'hostname': 'devops01.lab',
        'ip': '172.16.1.73',
        'netmask': '255.255.255.0',
        'gateway': '172.16.1.1',
        'interface': 'eth0'
    },
    'intranet': {
        'hostname': 'intranet.lab',
        'ip': '172.16.1.74',
        'netmask': '255.255.255.0',
        'gateway': '172.16.1.1',
        'interface': 'eth0'
    }
}


def run_command(cmd: list, description: str = "") -> tuple:
    try:
        logger.info(f"Executing: {description or ' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            logger.warning(f"Command failed: {result.stderr}")
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        logger.error(f"Error running command: {str(e)}")
        return 1, "", str(e)


def set_hostname(hostname: str) -> bool:
    cmd = ['hostnamectl', 'set-hostname', hostname]
    returncode, stdout, stderr = run_command(cmd, f"Setting hostname to {hostname}")
    
    if returncode == 0:
        logger.info(f"Hostname set to: {hostname}")
        return True
    else:
        logger.error(f"Failed to set hostname: {stderr}")
        return False


def configure_network_interface(interface: str, ip: str, netmask: str, gateway: str) -> bool:
    try:
        config_file = f'/etc/sysconfig/network-scripts/ifcfg-{interface}'
        
        config_content = f"""TYPE=Ethernet
DEVICE={interface}
ONBOOT=yes
BOOTPROTO=none
IPADDR={ip}
NETMASK={netmask}
GATEWAY={gateway}
DNS1=8.8.8.8
DNS2=8.8.4.4
"""
        
        logger.info(f"Writing network config to {config_file}")
        
        cmd = ['tee', config_file]
        result = subprocess.run(cmd, input=config_content, capture_output=True, 
                               text=True, check=False)
        
        if result.returncode != 0:
            logger.error(f"Failed to write network config: {result.stderr}")
            return False
        
        logger.info(f"Restarting network service for {interface}")
        restart_cmd = ['nmcli', 'connection', 'reload']
        returncode, stdout, stderr = run_command(restart_cmd, "Reloading network connections")
        
        if returncode != 0:
            logger.warning("nmcli reload failed, trying service restart")
            restart_cmd = ['systemctl', 'restart', 'network']
            returncode, stdout, stderr = run_command(restart_cmd, "Restarting network service")
        
        return returncode == 0
        
    except Exception as e:
        logger.error(f"Error configuring network: {str(e)}")
        return False


def update_hosts_file(hostname: str, ip: str) -> bool:
    try:
        hosts_file = '/etc/hosts'
        
        try:
            with open(hosts_file, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            logger.error(f"{hosts_file} not found")
            return False
        
        entry = f"{ip}\t{hostname}"
        for line in lines:
            if line.strip().startswith(ip) or hostname in line:
                logger.info(f"Entry already exists in {hosts_file}")
                return True
        
        with open(hosts_file, 'a') as f:
            f.write(f"\n{entry}\n")
        
        logger.info(f"Added {hostname} ({ip}) to {hosts_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error updating /etc/hosts: {str(e)}")
        return False


def verify_configuration(hostname: str, ip: str) -> bool:
    try:
        returncode, current_hostname, _ = run_command(['hostnamectl', '--static'], 
                                                      "Verifying hostname")
        if returncode != 0 or current_hostname.strip() != hostname:
            logger.error(f"Hostname verification failed. Expected: {hostname}, Got: {current_hostname.strip()}")
            return False
        
        logger.info(f"Hostname verified: {hostname}")
        
        try:
            with open('/etc/hosts', 'r') as f:
                content = f.read()
                if ip in content and hostname in content:
                    logger.info(f"IP address verified in /etc/hosts")
                    return True
        except FileNotFoundError:
            logger.warning("/etc/hosts not found for verification")
            return False
            
    except Exception as e:
        logger.error(f"Error verifying configuration: {str(e)}")
        return False


def configure_hostname(server_type: str) -> bool:
    if server_type not in SERVER_CONFIG:
        logger.error(f"Unknown server type: {server_type}")
        logger.info(f"Available servers: {', '.join(SERVER_CONFIG.keys())}")
        return False
    
    config = SERVER_CONFIG[server_type]
    hostname = config['hostname']
    ip = config['ip']
    netmask = config['netmask']
    gateway = config['gateway']
    interface = config['interface']
    
    logger.info(f"Starting configuration for {server_type}:")
    logger.info(f"  Hostname: {hostname}")
    logger.info(f"  IP: {ip}")
    logger.info(f"  Interface: {interface}")
    
    if not set_hostname(hostname):
        logger.error("Failed to set hostname")
        return False
    
    if not configure_network_interface(interface, ip, netmask, gateway):
        logger.error("Failed to configure network interface")
        return False
    
    if not update_hosts_file(hostname, ip):
        logger.error("Failed to update /etc/hosts")
        return False
    
    if not verify_configuration(hostname, ip):
        logger.error("Configuration verification failed")
        return False
    
    logger.info(f"Configuration for {server_type} completed successfully!")
    return True
