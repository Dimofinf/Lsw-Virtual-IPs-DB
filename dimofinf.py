# Lsw-Virtual-IPs-DB
# v1.0
# Dimofinf, Inc
# # # # # # # # # #

import requests
import json
import xlsxwriter

serverslimit = "1000"
apiurl = "https://api.leaseweb.com/v1/virtualServers?limit=" + serverslimit
apikey = ''
headers = {"X-Lsw-Auth": apikey}
debug = 0
export_file = "servers.xlsx"  # Final file delivered

# Open XLSX file and adding sheets
workbook = xlsxwriter.Workbook(export_file)
worksheet_servers_details = workbook.add_worksheet("Servers IPs")

# Formatting CELLS
cells_titles_format = workbook.add_format({'bold': True})
cells_titles_format.set_bg_color("#81BEF7")

# Declaring Awesome variables for columns
virtual_name_col = 0
virtual_ip_col = 1
row_count = 1

# Set width for column
worksheet_servers_details.set_column(virtual_name_col, virtual_name_col, 16)
worksheet_servers_details.set_column(virtual_ip_col, virtual_ip_col, 20)

# Format to write ( row, column, content, format )
worksheet_servers_details.write(0, virtual_name_col, "ServerName", cells_titles_format)
worksheet_servers_details.write(0, virtual_ip_col, "ServerIP", cells_titles_format)

# Get list of servers
try:
    response = requests.get(apiurl, headers=headers)
    content = response.text
    content_json = json.loads(content)
    servers_number = len(content_json["virtualServers"])

    print("Please wait for a while until we get your IPs pool from leaseweb.")
    for count in range(servers_number):
        virtual_json = content_json["virtualServers"][count]
        virtual_id = virtual_json["id"]
        virtual_name = virtual_json["serverName"]
        virtual_ip = virtual_json["ipAddresses"]

        percentage = 100 * (int(count)/int(servers_number))
        print("Loading : %d %%" % (int(percentage)))

        if debug == 1:
            print("Generating information of : " + virtual_name)
            print(virtual_name)

        worksheet_servers_details.write(row_count, virtual_name_col, virtual_name)
        # Loop onto IPs list and filter it out in a clean list
        for ip in virtual_ip:
            ipaddr = ip["ip"]
            if debug == 1:
                print(ipaddr)

            worksheet_servers_details.write(row_count, virtual_ip_col, ipaddr)
            row_count += 1

        print("==============")


except any:
    pass

# Close the final XLSX file
workbook.close()
print("\nDone")
