import subprocess


def get_yes_no_input(prompt):
    while True:
        user_input = input(prompt).strip().lower()  # Get user input and normalize to lowercase
        if user_input in ['yes', 'y']:
            return True
        elif user_input in ['no', 'n']:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


# Command to be executed
command = "rpm -qi rsyslog"
# Result variable initialization.
result = ""
# Run the command and capture its output
try:
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')  # Decode the byte output to string
    # If you want to capture errors as well:
    errors = result.stderr.decode('utf-8')
    # print("Output:\n", output)
    for line in result.stdout.decode('utf-8').splitlines():
        if "Vendor" in line:
            vendor = line.split(":", 1)[1].strip()
            # Check vendor
            if vendor!="Red Hat, Inc.":
                print("The installed package is a third party package.")
                print("Please do reach out to respective vendor as not supported by Red Hat.")
            else:
                print("You already have RHEL shipped rsyslog package installed")
            break

except subprocess.CalledProcessError as e:
    print("Package rsyslog is not installed")
    
# Install package if not installed
if result == "":
    
    install_cnf = get_yes_no_input("Do you want to install? (yes/no): ")
    if install_cnf:
        print("installing rsyslog...")
        install_command = "yum install rsyslog -y"
        try:
            install_output = subprocess.run(install_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            install_success = install_output.stdout.decode('utf-8')
            install_errors = install_output.stderr.decode('utf-8')
            if install_success:
                print("Installed rsyslog successfully. :)")
            else: 
                print(install_errors)
        except subprocess.CalledProcessError as er:
            print("Error output:\n", er.stderr.decode('utf-8'))
    else:
        print("Abort")
# Install package if not installed

# validate the configuration.
print("Validating the existing configuration...")
base_conf_check = "rsyslogd -N3"
try:
    base_conf_check_result = subprocess.run(base_conf_check, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    base_conf_check_output = base_conf_check_result.stdout.decode('utf-8')  # Decode the byte output to string
    base_conf_check_error = base_conf_check_result.stderr.decode('utf-8')  # Decode the byte error to string
    print("All good to go.")
except subprocess.CalledProcessError as e:
    if "error" in e.stderr.decode('utf-8'):
        print(e.stderr.decode('utf-8'))

        
    
    