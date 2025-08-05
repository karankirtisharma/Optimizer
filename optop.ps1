Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Application]::EnableVisualStyles()

# Main Form
$form = New-Object System.Windows.Forms.Form
$form.Text = " PC Optimizer"
$form.Size = New-Object System.Drawing.Size(350, 450)
$form.StartPosition = "CenterScreen"

# Functions
function Clean-Temp {
    Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
    [System.Windows.Forms.MessageBox]::Show("Temp files cleaned.")
}

function Clear-RecycleBin {
    Clear-RecycleBin -Force -ErrorAction SilentlyContinue
    [System.Windows.Forms.MessageBox]::Show("Recycle Bin emptied.")
}

function Clear-Prefetch {
    Remove-Item "C:\Windows\Prefetch\*" -Recurse -Force -ErrorAction SilentlyContinue
    [System.Windows.Forms.MessageBox]::Show("Prefetch cleared.")
}

function Flush-DNS {
    ipconfig /flushdns | Out-Null
    [System.Windows.Forms.MessageBox]::Show("DNS cache flushed.")
}

function Clear-EventLogs {
    wevtutil el | ForEach-Object { wevtutil cl $_ } 
    [System.Windows.Forms.MessageBox]::Show("Event logs cleared.")
}

function Disable-BackgroundApps {
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" -Name GlobalUserDisabled -Value 1
    [System.Windows.Forms.MessageBox]::Show("Background apps disabled.")
}

function Restart-Explorer {
    Stop-Process -Name explorer -Force
    Start-Process explorer.exe
    [System.Windows.Forms.MessageBox]::Show("Windows Explorer restarted.")
}

function Free-RAM {
    $path = Join-Path $PSScriptRoot "EmptyStandbyList.exe"
    if (Test-Path $path) {
        Start-Process $path -ArgumentList "standbylist"
        [System.Windows.Forms.MessageBox]::Show("RAM standby list cleared.")
    } else {
        [System.Windows.Forms.MessageBox]::Show("EmptyStandbyList.exe not found.")
    }
}

# Buttons
$buttons = @(
    @{Text=" Clean Temp"; Action={Clean-Temp}},
    @{Text=" Clear Recycle Bin"; Action={Clear-RecycleBin}},
    @{Text=" Clear Prefetch"; Action={Clear-Prefetch}},
    @{Text=" Flush DNS"; Action={Flush-DNS}},
    @{Text=" Clear Event Logs"; Action={Clear-EventLogs}},
    @{Text=" Disable Background Apps"; Action={Disable-BackgroundApps}},
    @{Text=" Restart Explorer"; Action={Restart-Explorer}},
    @{Text=" Free RAM"; Action={Free-RAM}}
)

# Add Buttons Dynamically
$y = 20
foreach ($b in $buttons) {
    $btn = New-Object System.Windows.Forms.Button
    $btn.Text = $b.Text
    $btn.Size = New-Object System.Drawing.Size(280, 35)
    $btn.Location = New-Object System.Drawing.Point(30, $y)
    $btn.Add_Click($b.Action)
    $form.Controls.Add($btn)
    $y += 40
}

# Run
[void]$form.ShowDialog()
