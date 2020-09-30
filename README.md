<img src="Images/astro.png" align="right" align="right" height="200" />

# [Astro - Discord Bot](https://asksirk.com/Astro)
<p>
  <img src="https://img.shields.io/discord/743121194911531110">
  <img src="https://img.shields.io/github/contributors/ISIRK/Astro?style=flat">
  <img src="https://img.shields.io/github/last-commit/ISIRK/Astro">
  <img src="https://img.shields.io/github/v/release/ISIRK/Astro?include_prereleases&style=flat">
<p>

<br>
A Private Utilities Discord Bot with reliability and simplicity<br>

This Bot is a Private Discord Bot but you can request Astro Bot for your server by DM'ing me @ isirk#0001<br>
You can also request some commands by joining our support discord server.<br>
<br>

**Format for requesting Astro for your server:**

` Name:(Discord Tag)`<br>
` Server Name:`<br>
` Server Invite:`<br>
` Ammount of Members:`<br>
` Why you want Astro in your server:`<br>
` (Optional)Any other thing you want me to know?`

**To submit an Application please DM me on [Discord](https://discord.com) @ isirk#0001**

[Patreon](https://www.patreon.com/Astro_Bot)

[Astro Site](https://asksirk.com/Astro/)

[Support Discord Server](https://discord.gg/s5ZPSRe)

## Contribute
#### We suggest that instead of self-hosting Astro you have us Host it. To request Astro for your server see above.
**Make sure that you have the latest version of [python](https://www.python.org/) downloaded**
1. Fork the repository
2. Clone the repository & install required dependencies:
```
$ git clone git@github.com:YOUR_GITHUB_USERNAME/Astro
$ python -m pip install -U discord.py
```
3. Create a `.json` file in the root directory of the project paste the following code:
```json
{
"TOKEN" : "YOUR_TOKEN_HERE",
"PREFIX" : ["PREFIX" , "PREFIX" , "PREFIX"]
}
```
and replace `YOUR_TOKEN_HERE` with a new bot token from https://discord.com/developers/applications

4. In Astro/astro.py line #7 (Lines Below); Change `tokenFile = "/home/pi/Astro/Astro/.json"` to the path leading to your `.json` file.
```py
##CONFIG
tokenFile = "/home/pi/Astro/Astro/.json"
with open(tokenFile) as f:
    data = json.load(f)
token = data['TOKEN']
prefixes = data['PREFIX']
```

### Prerequisites
- [Python](https://www.python.org/)
- [Discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
