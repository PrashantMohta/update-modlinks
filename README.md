Creates an MR to your local modlinks with the latest release of your mod

Example usage:

```yml
on:
  push:
    tags:
      - '*'

name: on-new-release-raise-modlinks-mr

jobs:
  send-pull-requests:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@ac593985615ec2ede58e132d2e21d2b1cbd6127c # v3.3.0
        with:
          fetch-depth: 0 
          ref: ${{github.event.pull_request.head.ref}}
          repository: ${{github.event.pull_request.head.repo.full_name}}
          token: ${{secrets.GITHUB_TOKEN}}
      - name: Update into modlinks and send pull-request
        uses: PrashantMohta/update-modlinks@v1
        with:
          access-token: ${{secrets.ACCESS_TOKEN}}
          project-name: ${{vars.PROJECT_NAME}}
          user-name: ${{vars.USER_NAME }}
          user-email: ${{vars.USER_EMAIL }}
          asset-name: ${{vars.ASSET_NAME}}
        
```