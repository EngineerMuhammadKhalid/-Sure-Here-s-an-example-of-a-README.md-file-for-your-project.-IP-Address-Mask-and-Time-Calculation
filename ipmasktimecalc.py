import ipaddress

def validate_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def calculate_mask_and_time(nodes, k, initial_mask, final_mask):
    def ip_to_binary(ip):
        return ''.join(format(int(x), '08b') for x in ipaddress.IPv4Address(ip).packed)

    def calculate_saved_time(subnet1, subnet2):
        diff_bits = bin(subnet1 ^ subnet2).count('1')
        return max(1, diff_bits // 2)

    binary_ips = [ip_to_binary(node) for node in nodes]

    subnet_masks = []
    saved_times = set()

    for subnet_mask in range(initial_mask, final_mask + 1):
        current_mask = subnet_mask
        subnet_masks.append(current_mask)
        times_for_this_mask = set()

        for i in range(k):
            for j in range(i + 1, k):
                times_for_this_mask.add(calculate_saved_time(subnet_masks[i], subnet_masks[j]))

        saved_times.update(times_for_this_mask)

    return subnet_masks, sorted(saved_times, reverse=True)


def main(input_file, output_file):
    with open(input_file, 'r') as f_input, open(output_file, 'w') as f_output:
        t = int(f_input.readline().strip())
        for test_case in range(1, t + 1):
            f_output.write(f"Test Case #{test_case}:\n")
            try:
                n, k = map(int, f_input.readline().split())
                nodes = [f_input.readline().strip() for _ in range(n)]
                initial_mask, final_mask = map(int, f_input.readline().split())

                invalid_ips = [ip for ip in nodes if not validate_ip(ip)]
                if invalid_ips:
                    f_output.write("Invalid IP addresses found in the input.\n")
                    for ip in invalid_ips:
                        f_output.write(f"Invalid IP: {ip}\n")
                    continue

                masks, saved_times = calculate_mask_and_time(nodes, k, initial_mask, final_mask)

                for mask in masks:
                    f_output.write('.'.join([str((mask >> (8 * i)) & 255) for i in range(3, -1, -1)]) + '\n')
                for time in saved_times:
                    f_output.write(str(time) + '\n')

            except ValueError:
                f_output.write("Invalid input format in the test case.\n")
            except Exception as e:
                f_output.write(f"Error encountered in Test Case #{test_case}: {str(e)}\n")


if __name__ == "__main__":
    input_filename = 'newinput.txt'  # Change this to your input file name
    output_filename = 'output12.txt'  # Change this to your output file name
    main(input_filename, output_filename)
