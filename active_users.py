def get_active_users(passwd_file='/etc/passwd'):
    active_users = []

    try:
        with open(passwd_file, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) > 6:
                    username = parts[0]
                    shell = parts[6]
                    # Check if the user's shell is not /bin/false or /sbin/nologin (common shells for disabled accounts)
                    if shell not in ['/bin/false', '/sbin/nologin']:
                        active_users.append(username)
        return active_users

    except FileNotFoundError:
        print(f'Error: The file {passwd_file} was not found.')
    except PermissionError:
        print(f'Error: Permission denied when trying to read {passwd_file}.')

def main():
    users = get_active_users()
    if users:
        print('Active users on the system:')
        for user in users:
            print(user)
    else:
        print('No active users found or an error occurred.')

if __name__ == '__main__':
    main()