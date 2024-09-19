## Features

- 継続起動
  - Systemd に登録することでエラー終了しても自動で再起起動する
- 自動終了
  - プレイ人数が少なくなると自動でサーバを shutdown する

### WIP

- 自動終了時にバックアップもする
- EC2 の起動を CloudFlare Workers でする
- EC2 起動時に DDNS の更新をする(Workers 内でやってもいいかも？)
