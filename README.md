Quick OWASP-ZAP Active Rule script to test for CVE-2021-44228

Spams a payload to every parameter. If your callback listener lights up, then it's most likely vulnerable.

Could be adapted to test request headers.

Use with ATTACK Mode.  Not recommended for Active Scanning because it would be difficult to figure out which
payload(s) trigger a callback.

How to use:
1. Load this rule into ZAP under `Active Rules`
2. Set up a listener on an IP that the target can reach (e.g. netcat)
3. Replace LISTENER_IP and LISTENER_PORT with your listener's IP/PORT
4. Save/Enable the script
5. Set up a scan policy with everything off except for `Script Active Scan Rules (Threshold Low/Strength Insane)`
6. Add target to scope
7. Switch to ATTACK Mode
8. Explore the site while monitoring the listener and see what requests/params trigger the callback

Use only against targets that you own or have explicit permission test.  The author of this script accepts no liability
or responsibility for the use of this script.

Twitter: @tdotfish

Github: https:github.com/tdotfish

Web: https:tdot.fish/
