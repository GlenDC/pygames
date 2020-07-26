# Ping Runner

An infinite runner inspired by the _POSIX_ `ping` command.
Or should I say: "A gamification of ping", because
if you have to ping you might as well have fun doing so :)

### How it generates levels?

Take the following ping example:

```bash
$ ping  -i 0.25  www.wikipedia.com
PING ncredir-lb.wikimedia.org (91.198.174.194): 56 data bytes
64 bytes from 91.198.174.194: icmp_seq=0 ttl=53 time=90.501 ms
64 bytes from 91.198.174.194: icmp_seq=1 ttl=53 time=109.579 ms
64 bytes from 91.198.174.194: icmp_seq=2 ttl=53 time=78.892 ms
Request timeout for icmp_seq 3
64 bytes from 91.198.174.194: icmp_seq=3 ttl=53 time=260.479 ms
64 bytes from 91.198.174.194: icmp_seq=4 ttl=53 time=45.700 ms
64 bytes from 91.198.174.194: icmp_seq=5 ttl=53 time=150.345 ms
64 bytes from 91.198.174.194: icmp_seq=6 ttl=53 time=129.957 ms
^C
--- ncredir-lb.wikimedia.org ping statistics ---
7 packets transmitted, 7 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 45.700/123.636/260.479/64.199 ms
```

- request timeouts are used to generate gaps in the floor;
- the successful requests generate obstacles to jump over/through;

In practical terms, one can imagine the following to generate something
such as the following:

```
                                         +
            ⇴         ⇴         ⇴       ⇴               ⇴
          ⇴   ⇴     ⇴   ⇴     ⇴   ⇴   ⇴   ⇴           ⇴ + ⇴
P ⇴⇴⇴⇴⇴⇴⇴⇴  |   ⇴⇴⇴   |  ⇴⇴⇴⇴⇴     ⇴⇴⇴   | ⇴⇴⇴⇴⇴⇴⇴⇴⇴⇴⇴  |  ⇴⇴⇴⇴
------------+---------+--------   -------+--------------+-- ...
```

The exact parameters used to actually generate the terrain
will depend upon the current difficulty level, and are either
way up for iteration.

Finally the stats reported at the end can be displayed
as extra info in the score display scene.

The IP pinged can also be used to estimate a location,
and as such use it for extra fun purposes. Game candy if you will.
