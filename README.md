# mawinter-gss

- 家計簿API の https://github.com/azuki774/mawinter-server の情報を Google Spread Sheetに表示、定期反映するソフト。

- スプレッドシートのA列に `category_id` が記載されている行を、[ `category_id`, `category_name`, `4月の額`, `5月の額`, ... , `3月の額`] に変更する（その行含めて、それ以外のセルは上書きしない）

- コンテナ内の `/.secret/credential.json` （リポジトリ内では `deployment/gss/.secret/credential.json`）に、GSS の サービスアカウント用のシークレットJSON を配置する。
## 環境変数
```
    environment:
      - MAWINTER_API_ENDPOINT="mock" # mawinter-api の /v2/record/summary/YYYY のエンドポイント。`mock` を入れると、ダミーデータを代わりに挿入する。
      - SPREADSHEET_URL="" # スプレッドシートのURL
      - WORKSHEET_NAME="" # ワークシートの名前
      - JOB_INTERVAL="30" # 更新する頻度（分）
```
