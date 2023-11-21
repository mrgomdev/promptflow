<#
.DESCRIPTION
Script to build doc site

.EXAMPLE 
PS> ./doc_generation.ps1 -SkipInstall # skip pip install
PS> ./doc_generation.ps1 -BuildLinkCheck -WarningAsError:$true -SkipInstall

#>
[CmdletBinding()]
param(
    [switch]$SkipInstall,
    [switch]$WarningAsError = $false,
    [switch]$BuildLinkCheck = $false,
    [switch]$WithReferenceDoc = $false
)

[string] $ScriptPath = $PSCommandPath | Split-Path -Parent
[string] $RepoRootPath = $ScriptPath | Split-Path -Parent | Split-Path -Parent
[string] $DocPath = [System.IO.Path]::Combine($RepoRootPath, "docs")
[string] $TempDocPath = New-TemporaryFile | % { Remove-Item $_; New-Item -ItemType Directory -Path $_ }
[string] $PkgSrcPath = [System.IO.Path]::Combine($RepoRootPath, "src\promptflow\promptflow")
[string] $OutPath = [System.IO.Path]::Combine($ScriptPath, "_build")
[string] $SphinxApiDoc = [System.IO.Path]::Combine($DocPath, "sphinx_apidoc.log")
[string] $SphinxBuildDoc = [System.IO.Path]::Combine($DocPath, "sphinx_build.log")
[string] $WarningErrorPattern = "WARNING:|ERROR:|CRITICAL:"
$apidocWarningsAndErrors = $null
$buildWarningsAndErrors = $null

if (-not $SkipInstall){
    # Prepare doc generation packages
    pip install pydata-sphinx-theme==0.11.0
    pip install sphinx==5.1
    pip install sphinx-copybutton==0.5.0
    pip install sphinx_design==0.3.0
    pip install sphinx-sitemap==2.2.0
    pip install sphinx-togglebutton==0.3.2
    pip install sphinxext-rediraffe==0.2.7
    pip install sphinxcontrib-mermaid==0.8.1
    pip install ipython-genutils==0.2.0
    pip install myst-nb==0.17.1
    pip install numpydoc==1.5.0
    pip install myst-parser==0.18.1
    pip install matplotlib==3.4.3
    pip install jinja2==3.0.1
    Write-Host "===============Finished install requirements==============="
}


function ProcessFiles {
    # Exclude files not mean to be in doc site
    $exclude_files = "README.md", "dev"
    foreach ($f in $exclude_files)
    {
        $full_path = [System.IO.Path]::Combine($TempDocPath, $f)
        Remove-Item -Path $full_path -Recurse
    }
}

Write-Host "===============PreProcess Files==============="
Write-Host "Copy doc to: $TempDocPath"
ROBOCOPY $DocPath $TempDocPath /S /NFL /NDL /XD "*.git" [System.IO.Path]::Combine($DocPath, "_scripts\_build")
ProcessFiles

if($WithReferenceDoc){
    $RefDocRelativePath = "reference\python-library-reference"
    $RefDocPath = [System.IO.Path]::Combine($TempDocPath, $RefDocRelativePath)
    if(!(Test-Path $RefDocPath)){
        throw "Reference doc path not found. Please make sure '$RefDocRelativePath' is under '$DocPath'"
    }
    Remove-Item $RefDocPath -Recurse -Force
    Write-Host "===============Build Promptflow Reference Doc==============="
    sphinx-apidoc --module-first --no-headings --no-toc --implicit-namespaces "$PkgSrcPath" -o "$RefDocPath" | Tee-Object -FilePath $SphinxApiDoc 
    $apidocWarningsAndErrors = Select-String -Path $SphinxApiDoc -Pattern $WarningErrorPattern

    Write-Host "=============== Overwrite promptflow.connections.rst ==============="
    # We are doing this overwrite because the connection entities are also defined in the promptflow.entities module
    # and it will raise duplicate object description error if we don't do so when we run sphinx-build later.
    $ConnectionRst = [System.IO.Path]::Combine($RepoRootPath, "scripts\docs\promptflow.connections.rst")
    $AutoGenConnectionRst = [System.IO.Path]::Combine($RefDocPath, "promptflow.connections.rst")
    Copy-Item -Path $ConnectionRst -Destination $AutoGenConnectionRst -Force
}


Write-Host "===============Build Documentation with internal=${Internal}==============="
$BuildParams = [System.Collections.ArrayList]::new()
if($WarningAsError){
    $BuildParams.Add("-W")
    $BuildParams.Add("--keep-going")
}
if($BuildLinkCheck){
    $BuildParams.Add("-blinkcheck")
}
$Env:DOC_VERSION = "Python"
$PYTHON_DOC = [System.IO.Path]::Combine($TempDocPath, "python")
$PYTHON_DOC_OUT = [System.IO.Path]::Combine($OutPath, "python")
sphinx-build $PYTHON_DOC $PYTHON_DOC_OUT -c $ScriptPath $BuildParams | Tee-Object -FilePath $SphinxBuildDoc
$Env:DOC_VERSION = "C#"
$CSHARP_DOC = [System.IO.Path]::Combine($TempDocPath, "csharp")
$CSHARP_DOC_OUT = [System.IO.Path]::Combine($OutPath, "csharp")
sphinx-build $CSHARP_DOC $CSHARP_DOC_OUT -c $ScriptPath $BuildParams | Tee-Object -FilePath $SphinxBuildDoc
$Env:DOC_VERSION = "Javascript"
$JS_DOC = [System.IO.Path]::Combine($TempDocPath, "js")
$JS_DOC_OUT = [System.IO.Path]::Combine($OutPath, "js")
sphinx-build $JS_DOC $JS_DOC_OUT -c $ScriptPath $BuildParams | Tee-Object -FilePath $SphinxBuildDoc
# Copy 404 files.
[string] $404Path = [System.IO.Path]::Combine($DocPath, "404.html")
[string] $Raw404Path = [System.IO.Path]::Combine($DocPath, "404NotFound.html")
[string] $IndexPath = [System.IO.Path]::Combine($DocPath, "index.html")
Copy-Item -Path $404Path -Destination $OutPath -Force
Copy-Item -Path $Raw404Path -Destination $OutPath -Force
Copy-Item -Path $IndexPath -Destination $OutPath -Force
$buildWarningsAndErrors = Select-String -Path $SphinxBuildDoc -Pattern $WarningErrorPattern

Write-Host "Clean path: $TempDocPath"
Remove-Item $TempDocPath -Recurse -Confirm:$False -Force

if ($apidocWarningsAndErrors) {  
    Write-Host "=============== API doc warnings and errors ==============="  
    foreach ($line in $apidocWarningsAndErrors) {  
        Write-Host $line -ForegroundColor Red  
    }  
}  
  
if ($buildWarningsAndErrors) {  
    Write-Host "=============== Build warnings and errors ==============="  
    foreach ($line in $buildWarningsAndErrors) {  
        Write-Host $line -ForegroundColor Red  
    }  
} 