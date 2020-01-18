Crontab:
-------

# spaceapi
29 * * * *      /home/space/bin/update-spaceapi.py
29 0 * * *      /home/space/bin/set-timezones.py
*/10 * * * *    /home/space/bin/get-spaceapi.py



(c) 2014-2020 by Folkert van Heusden <mail@vanheusden.com>
