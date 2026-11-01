<#
Day 12: Windows Event Summary Tool
Purpose:    Collect limited metadata from selected Windows event logs.
Scope:      Read-only inspection of the local computer.
Privacy:    Full event messages are intentionally not collected.
Limitations:This is a basic inventory tool, not a SIEM or
            automated security verdict.
#>

[CmdletBinding()]
param(
    [ValidateRange(1, 168)]
    [int]$HoursBack = 24,

    [ValidateRange(1, 500)]
    [int]$MaxEventsPerLog = 100
)

$ErrorActionPreference = "Continue"
$StartTime = (Get-Date).AddHours(-$HoursBack)

$OutputDirectory = Join-Path $PSScriptRoot "..\private-output"
$OutputDirectory = [System.IO.Path]::GetFullPath($OutputDirectory)

New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

$Queries = @(
    @{
        LogName = "System"
        EventIds = @()
    },
    @{
        LogName = "Application"
        EventIds = @()
    },
    @{
        LogName = "Security"
        EventIds = @(4624, 4625, 4672, 4688, 1102)
    }
)

$CollectedEvents = @()

foreach ($Query in $Queries) {
    Write-Host ""
    Write-Host "Inspecting log: $($Query.LogName)"

    $Filter = @{
        LogName = $Query.LogName
        StartTime = $StartTime
    }

    if ($Query.EventIds.Count -gt 0) {
        $Filter["Id"] = $Query.EventIds
    }

    try {
        $Events = Get-WinEvent -FilterHashtable $Filter -MaxEvents $MaxEventsPerLog -ErrorAction Stop

        foreach ($Event in $Events) {
            $CollectedEvents += [PSCustomObject]@{
                LogName     = $Query.LogName
                TimeCreated = $Event.TimeCreated
                EventId     = $Event.Id
                Provider    = $Event.ProviderName
                Level       = $Event.LevelDisplayName
                RecordId    = $Event.RecordId
            }
        }
        Write-Host "Query completed."
    }
    catch {
        Write-Warning (
            "Could not retrieve matching records from " +
            "$($Query.LogName). This may indicate no matching " +
            "events, unavailable data, or restricted access. " +
            $_.Exception.Message
        )
    }
}

Write-Host ""
Write-Host "===== COLLECTION SUMMARY ====="
Write-Host "Hours examined: $HoursBack"
Write-Host "Maximum events per query: $MaxEventsPerLog"
Write-Host "Records collected: $($CollectedEvents.Count)"

if ($CollectedEvents.Count -gt 0) {
    $CsvPath = Join-Path $OutputDirectory "event-metadata.csv"

    $CollectedEvents |
        Sort-Object TimeCreated |
        Export-Csv -Path $CsvPath -NoTypeInformation -Encoding UTF8

    Write-Host ""
    Write-Host "Event counts by log and Event ID:"
    $CollectedEvents |
        Group-Object LogName, EventId |
        Sort-Object Count -Descending |
        Select-Object Count, Name |
        Format-Table -AutoSize

    Write-Host ""
    Write-Host "Local report created:"
    Write-Host $CsvPath
} else {
    Write-Warning "No event records were collected. Check log availability, time range, and permissions."
}

Write-Host ""
Write-Host "Collection completed."
Write-Host "This output is an event inventory, not a malware verdict."