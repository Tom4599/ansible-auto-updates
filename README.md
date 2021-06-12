# ansible-auto-updates

This project is entirely public, and therefore special attention must be paid to the quality of the code and the information present in it.

## Requirements

You need to have 3 inventory groups (even if they're empty) :

```
[auto_updates_preprod]
debian10
centos7
ubuntu18
centos8

[auto_updates_uat]

[auto_updates_prod]
```

## Description and basic usage

This role allows to enable auto-updates and deploy specific configuration.

You can basically use it by appending the role to your ansible project :

``` yaml
- hosts : all
  roles:
    - { role: ansible-auto-updates }
```

## Targets

- Debian >= 9
- Ubuntu >= 18
- CentOS >= 7

The targets are splitted in 3 groups:
- `auto_updates_uat`
- `auto_updates_preprod`
- `auto_updates_prod`

### Differences between OSes

There are a few differences between OSes, and minor differences between
different versions.

* On Debian and Ubuntu, we install unattended-upgrades with specific configuration and a timer to set execution time.
* On RedHat
  * 6 : we install yum-cron and set configuration in /etc/sysconfig
  * 7 : we install yum-cron and set 2 different configuration in /etc/yum
For 6 and 7, the script is move to /usr/local/bin and we create a cron to allow us to set execution time
  * 8 : we install dnf-automatic, set configuration and a timer like Debian.

## Role variables

| Variable           | Description| Default value |
|--------------------|------------|---------------|
|auto_updates_mail|Mail to send notification.||
|auto_updates_blacklisted_packages|List of blacklisted packages.|Disabled|
|auto_updates_upgrade_frequency|Frequency of upgrades (monthly, weekly or daily).|monthly|
|auto_updates_start_upgrade_time|Start time for upgrade.|09:00:00|
|auto_updates_random_upgrade_time|Random time for upgrade (in minutes).|180|
|auto_updates_start_update_time|Start time for download.|08:00:00|
|auto_updates_random_update_time|Random time for download (in minutes).|50|
|auto_updates_policy|Policy for upgrade (security or updates)|security|

## Frequency details

Three frequencies have been configured (auto_updates_upgrade_frequency):

**Monthly :**

* auto_updates_uat : On first Monday of the month
* auto_updates_preprod: The day after (Tuesday)
* auto_updates_prod : 2 days after (Thursday)

**Weekly :**

* auto_updates_uat : Every Monday
* auto_updates_preprod : Every Tuesday
* auto_updates_prod : Every Thursday

**Daily :**

* The same for all groups : Every days except Friday, Saturday and Sunday

## Example :

```yaml
- hosts: all
  roles:
     - ansible-auto-updates
  vars:
    auto_updates_mail: tom.saunier@example.com
    auto_updates_blacklisted_packages:
      - vim
      - openssh*
    auto_updates_policy: updates
    auto_updates_upgrade_frequency: "weekly"
```
