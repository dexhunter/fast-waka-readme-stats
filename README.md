# ⚡️ fast-waka-readme-stats

## the *blazingly-fast* way to keep your GitHub profile fresh

Ever wondered **when** you crank out most of your code (🌞 morning or 🌙 night?),
what editor you really use, or how many lines you’ve shipped?  
This Action fetches data from **GitHub** & **WakaTime** **in parallel**, crunches it in seconds,  
and auto-injects an eye-catching stats section into your profile README.

Average runtime in CI: **< 30 s** for repos with hundreds of projects — check the proof in the sample run below.

---

## ✨ What you get

* 4-slot “morning / day / evening / night” commit heat-map  
* Top languages, editors, operating systems and projects for the last 7 days  
* Total lines-of-code badge **+** a LOC timeline chart  
* Profile-view counter, storage usage, public/private repo counts & more  
* 30 + locales, selectable symbol styles, fully toggleable sections

---

## 🔑 Prerequisites

| Secret / input            | Purpose                                  | Where to get it                      |
|---------------------------|------------------------------------------|--------------------------------------|
| **GH_TOKEN** (required)   | commit back to your profile repository   | `${{ github.token }}` or PAT         |
| **WAKATIME_API_KEY**      | pull your coding activity                | https://wakatime.com/settings        |

Add both under **Settings → Secrets → Actions**.

---

## 🚀 Quick start (minimal workflow)

```
    # .github/workflows/update-devmetrics.yml
    name: Update Dev Metrics
    on:
      schedule:
        - cron: '0 2 * * *'          # every day at 02:00 UTC
      workflow_dispatch:

    jobs:
      update-readme:
        runs-on: ubuntu-latest
        steps:
          - name: 🏃 Run waka-readme-stats
            uses: wakareadmestats/waka-readme-stats@master
            env:
              INPUT_GH_TOKEN: ${{ secrets.GH_TOKEN }}
              INPUT_WAKATIME_API_KEY: ${{ secrets.WAKATIME_API_KEY }}
```

The Action fills everything between these markers in your README.md:

    <!--START_SECTION:waka-->
    … stats will be generated here …
    <!--END_SECTION:waka-->

---

## 🛠 Full-power example

```
    steps:
      - name: Update Dev Metrics
        uses: wakareadmestats/waka-readme-stats@master
        env:
          INPUT_GH_TOKEN:                 ${{ secrets.GH_TOKEN }}
          INPUT_WAKATIME_API_KEY:         ${{ secrets.WAKATIME_API_KEY }}
          INPUT_SHOW_TIMEZONE:            "True"
          INPUT_SHOW_LANGUAGE:            "True"
          INPUT_SHOW_EDITORS:             "True"
          INPUT_SHOW_PROJECTS:            "True"
          INPUT_SHOW_OS:                  "True"
          INPUT_SHOW_COMMIT:              "True"
          INPUT_SHOW_DAYS_OF_WEEK:        "True"
          INPUT_SHOW_LINES_OF_CODE:       "True"
          INPUT_SHOW_LOC_CHART:           "True"
          INPUT_SHOW_PROFILE_VIEWS:       "True"
          INPUT_SHOW_TOTAL_CODE_TIME:     "True"
          INPUT_SHOW_LANGUAGE_PER_REPO:   "True"
          INPUT_COMMIT_BY_ME:             "True"
          INPUT_COMMIT_MESSAGE:           "chore: update dev metrics"
          INPUT_PUSH_BRANCH_NAME:         "main"
          INPUT_LOCALE:                   "en"
          INPUT_SYMBOL_VERSION:           "2"
```

Unset any flag (or set it to `"False"`) to hide that section.

---

## 🏎 Real-world run

See a full workflow using this Action — including logs that show it finishing
in under half a minute — here:  
https://github.com/dexhunter/dexhunter/actions/workflows/update-devmetrics.yml

---

## 🐞 Troubleshooting

* **Stats missing / zero %** → ensure WakaTime has activity for the last 7 days.  
* **Private repos ignored** → the token in `GH_TOKEN` needs `repo` scope.  
* **API rate-limits** → the Action auto-backs off; rerun later or use a PAT.

---

## 📜 License

MIT • Dex Hunter & contributors

## 🙏 Special thanks

Big shout-out to the original author Anmol Pratap Singh for creating the foundation this fork builds on.

