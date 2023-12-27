# DroneEngineer16
ドローンエンジニア養成塾16期 - アプリケーションコース課題

## 必要となるパッケージのインストール手順

### 1. Mission Plannnerのインストール
下記リンクをクリックして最新のインストーラをダウンロードします。 
https://firmware.ardupilot.org/Tools/MissionPlanner/MissionPlanner-latest.msi  

ダウンロードされたインストーラ `MissionPlanner-latest.msi` をダブルクリックします。  

ライセンスに同意して、基本的に`Next`、`Install`、`次へ`、`完了` を押下してインストールを完了させます。  

### 2. WSLのインストール
あまり古いバージョンのWindows10だとWSL機能が使えないため念の為バージョンを確認してください。  

WSLをインストールするためには、Windows 10 version 2004(Build 19041)以上、もしくはWindows 11である必要があります。古い場合はWindows10の更新、またはWindows 11のインストールを先に完了してから再度このステップから実行してください。  

#### Windowsの機能の有効化
管理者として`PowerShell`を開き、以下を実行します。

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

PC再起動後、PowerShellを開いて次のコマンドを実行しPowerShellを閉じてください。これでデフォルトのバージョンを1にします。  
デフォルトが1で困る場合は、WSLバージョン2でインストールした後で個別に `wsl --set-version Ubuntu-20.04 1` を実行して変更してください。
```powershell
wsl --set-default-version 1
```

#### Ubuntu20のインストールと初期設定
PowerShellを開いて次のコマンドを実行して`Ubuntu 20.04`をインストールしてください。

```powershell
wsl --install -d Ubuntu-20.04
```

インストールが完了したら `PCを再起動` をしてください。<br/>
PC起動後の初回起動時 `Installing, this may take a few minutes…` としばらく表示されます。フリーズではないので、そのままインストールが完了するまで待ちます。  
インストールが終わると username と password をきかれるので、下記の通り入力して設定します。必ず半角英字のみで設定します。

* username : `ardupilot`
* password : `ardupilot` 

パスワードは入力してもセキュリティ上表示されませんが入力されています。間違えた場合はバックスペースで消せます。


### 3. DroneKit Python セットアップ
Visual Studio Codeを起動しWSLに接続します。  
メニュー `ターミナル` → `新しいターミナル` を選択します。

#### pipのインストール
ターミナルタブに次のコマンドを順番に実行してください。パスワードや続行可否を聞かれるので、都度入力してください。  
```bash
sudo apt update
```
```bash
sudo apt install python3-pip
```
```bash
pip -V
```
下記のように表示されたら正常にインストールされています。  
```bash
pip 22.0.2 from /usr/lib/python3/dist-packages/pip (python 3.10)
```

#### DroneKit Python最新のソースコードからインストール
メニュー `ターミナル` → `新しいターミナル` を選択します。 -->
ターミナルタブに次のコマンドを順番に実行してください。
```bash
cd
```
```bash
git clone https://github.com/dronekit/dronekit-python
```
```bash
cd dronekit-python
```
```bash
pip3 install . --user
```
下記のような実行結果になれば正常にインストールが完了しています。  
```bash
Requirement already satisfied: monotonic>=1.3 in /home/ardupilot/.local/lib/
～省略～
Successfully built dronekit
Installing collected packages: dronekit
  Attempting uninstall: dronekit
    Found existing installation: dronekit 2.9.2
    Uninstalling dronekit-2.9.2:
      Successfully uninstalled dronekit-2.9.2
Successfully installed dronekit-2.9.2
```

## アプリケーション実行手順
Mission Plannner上部メニューの`シミュレーション`を押下して、シミュレーション画面に切り替え、シミュレータを起動してMission Plannerから接続します。  
本プログラムを実行することでシミュレーションが開始されます。

```python
# ドローンを離陸させる
target_altitude = 10  # 離陸したい高さ（メートル）
target_move_distance = 10 # 移動したい距離（メートル）
```
`course2.py`の35行目付近の変数設定で、離陸したい高さや移動距離を容易に変更可能です。
