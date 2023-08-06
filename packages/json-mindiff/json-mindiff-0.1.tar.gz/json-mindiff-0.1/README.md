# json-mindiff

Minimize diff introduced to json files by tools that treat json dictionary
as unordered hash map (kind of right thing to do but annoying anyway).

***WORK IN PROGRESS***

# Usage

The primary goal is to restrict `packer` from reformatting templates even when
there are no changes.

First make sure [templates](https://github.com/themalkolm/packer-templates) are
sane formatted, lets use `jq` for this. This way we make sure to have a fixed
base point to blame packer.

```
$ jq . template.json          > tmp && mv tmp template.json
$ jq . template.outdated.json > tmp && mv tmp template.outdated.json
```

Add current directory to PATH to make sure all examples work for you as well:

```
$ export PATH=${PATH}:$(pwd)
```

Here is the default `packer` behaviour (😠). There are no changes, packer simply
reformats the template:

```
$ packer fix template.json | jq . > template.json.new
$ diff template.json template.json.new
2,8d1
<   "min_packer_version": "1.2.0",
<   "variables": {
<     "box_file": "",
<     "iso_url": "",
<     "iso_checksum_type": "",
<     "iso_checksum": ""
<   },
11,14d3
<       "type": "virtualbox-iso",
<       "iso_url": "{{user `iso_url`}}",
<       "iso_checksum_type": "{{user `iso_checksum_type`}}",
<       "iso_checksum": "{{user `iso_checksum`}}",
19d7
<       "shutdown_command": "echo '/sbin/halt -h -p' > /tmp/shutdown.sh; echo 'vagrant'|sudo -S sh '/tmp/shutdown.sh'",
21d8
<       "guest_os_type": "RedHat_64",
22a10
>       "guest_os_type": "RedHat_64",
25c13,16
<       "ssh_port": 22,
---
>       "iso_checksum": "{{user `iso_checksum`}}",
>       "iso_checksum_type": "{{user `iso_checksum_type`}}",
>       "iso_url": "{{user `iso_url`}}",
>       "shutdown_command": "echo '/sbin/halt -h -p' > /tmp/shutdown.sh; echo 'vagrant'|sudo -S sh '/tmp/shutdown.sh'",
26a18
>       "ssh_port": 22,
29c21
<       "virtualbox_version_file": ".vbox_version",
---
>       "type": "virtualbox-iso",
43c35,45
<       ]
---
>       ],
>       "virtualbox_version_file": ".vbox_version"
>     }
>   ],
>   "min_packer_version": "1.2.0",
>   "post-processors": [
>     {
>       "compression_level": 9,
>       "keep_input_artifact": false,
>       "output": "{{user `box_file`}}",
>       "type": "vagrant"
48d49
<       "type": "shell",
59c60,61
<       }
---
>       },
>       "type": "shell"
62,69c64,69
<   "post-processors": [
<     {
<       "type": "vagrant",
<       "keep_input_artifact": false,
<       "compression_level": 9,
<       "output": "{{user `box_file`}}"
<     }
<   ]
---
>   "variables": {
>     "box_file": "",
>     "iso_checksum": "",
>     "iso_checksum_type": "",
>     "iso_url": ""
>   }
```

Here is the default `packer` behaviour piped through `json-mindiff` (🙂). There are no
changes and we keep it this way:

```
$ packer fix template.json | json-mindiff template.json | jq . > template.json.new
$ diff template.json template.json.new
```

Here is the fix `packer` behaviour (😠). Packer should fix `iso_md5` usage. Note that
it fixes and reformats, it is hard to see what is going on:

```
$ packer fix template.outdated.json | jq . > template.outdated.json.new
$ diff template.outdated.json template.outdated.json.new
2,7d1
<   "min_packer_version": "1.2.0",
<   "variables": {
<     "box_file": "",
<     "iso_url": "",
<     "iso_checksum": ""
<   },
10,12d3
<       "type": "virtualbox-iso",
<       "iso_url": "{{user `iso_url`}}",
<       "iso_md5": "{{user `iso_checksum`}}",
17d7
<       "shutdown_command": "echo '/sbin/halt -h -p' > /tmp/shutdown.sh; echo 'vagrant'|sudo -S sh '/tmp/shutdown.sh'",
19d8
<       "guest_os_type": "RedHat_64",
20a10
>       "guest_os_type": "RedHat_64",
23c13,16
<       "ssh_port": 22,
---
>       "iso_checksum": "{{user `iso_checksum`}}",
>       "iso_checksum_type": "md5",
>       "iso_url": "{{user `iso_url`}}",
>       "shutdown_command": "echo '/sbin/halt -h -p' > /tmp/shutdown.sh; echo 'vagrant'|sudo -S sh '/tmp/shutdown.sh'",
24a18
>       "ssh_port": 22,
27c21
<       "virtualbox_version_file": ".vbox_version",
---
>       "type": "virtualbox-iso",
41c35,45
<       ]
---
>       ],
>       "virtualbox_version_file": ".vbox_version"
>     }
>   ],
>   "min_packer_version": "1.2.0",
>   "post-processors": [
>     {
>       "compression_level": 9,
>       "keep_input_artifact": false,
>       "output": "{{user `box_file`}}",
>       "type": "vagrant"
46d49
<       "type": "shell",
57c60,61
<       }
---
>       },
>       "type": "shell"
60,67c64,68
<   "post-processors": [
<     {
<       "type": "vagrant",
<       "keep_input_artifact": false,
<       "compression_level": 9,
<       "output": "{{user `box_file`}}"
<     }
<   ]
---
>   "variables": {
>     "box_file": "",
>     "iso_checksum": "",
>     "iso_url": ""
>   }
```

Here is the fix `packer` behaviour piped through `json-mindiff` (🙂). Packer
should fix `iso_md5` usage. Note that diff is the absolute minimum.:

```
$ packer fix template.outdated.json | json-mindiff template.json | jq . > template.outdated.json.new
$ diff template.outdated.json template.outdated.json.new
12c12,13
<       "iso_md5": "{{user `iso_checksum`}}",
---
>       "iso_checksum_type": "md5",
>       "iso_checksum": "{{user `iso_checksum`}}",
```
