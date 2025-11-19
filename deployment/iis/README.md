# Enterprise AI Prompt Library - IIS Deployment Guide

Deploy the Enterprise AI Prompt Library to IIS with a single PowerShell command!

## Quick Start (One Command)

```powershell
# Run as Administrator from the repository root
.\deployment\iis\deploy.ps1
```

That's it! The script will automatically:

- ✅ Detect your Python installation
- ✅ Install all dependencies (Flask, wfastcgi, etc.)
- ✅ Create application directories
- ✅ Configure IIS and FastCGI
- ✅ Initialize the database with prompts
- ✅ Set correct permissions
- ✅ Start the website

**Access your site at**: `http://localhost`

### Custom Configuration

```powershell
# Custom port and location
.\deployment\iis\deploy.ps1 -Port 8080 -AppPath "D:\MyApps\prompt_library"

# With hostname
.\deployment\iis\deploy.ps1 -HostName "prompts.company.com" -Port 80
```

## Prerequisites

The deployment script will check and configure these automatically:

1. **Windows Server 2016 or higher**
2. **IIS 10.0 or higher** with CGI module (auto-installed by script)
3. **Python 3.8+** in your PATH
4. **Administrator privileges** (required to configure IIS)

## Manual Step-by-Step Deployment (If Needed)

### 1. Prepare Application Directory

```powershell
# Create application directory
New-Item -ItemType Directory -Path "C:\inetpub\wwwroot\prompt_library"
New-Item -ItemType Directory -Path "C:\inetpub\wwwroot\prompt_library\src"

# Copy application files (includes web.config)
Copy-Item -Path "src\*" -Destination "C:\inetpub\wwwroot\prompt_library\src" -Recurse

# Copy prompts directory (required by load_prompts.py)
Copy-Item -Path "prompts\*" -Destination "C:\inetpub\wwwroot\prompt_library\prompts" -Recurse
```

### 2. Install Dependencies

```powershell
cd C:\inetpub\wwwroot\prompt_library\src
pip install -r requirements.txt
```

### 3. Initialize Database

```powershell
python load_prompts.py
```

### 4. Enable wfastcgi

```powershell
wfastcgi-enable
```

This will output a script processor path like:

```text
C:\Python311\python.exe|C:\Python311\Lib\site-packages\wfastcgi.py
```

### 5. Configure IIS

#### Create New Site

1. Open **IIS Manager**
2. Right-click **Sites** → **Add Website**
3. Configure:
   - **Site name**: `Enterprise AI Prompt Library`
   - **Physical path**: `C:\inetpub\wwwroot\prompt_library\src`
   - **Port**: `80` (or desired port)
   - **Host name**: (optional, e.g., `prompts.yourcompany.com`)

#### Configure Application Pool

1. In IIS Manager, go to **Application Pools**
2. Find your application pool (same name as site)
3. Click **Advanced Settings**
4. Set:
   - **.NET CLR version**: `No Managed Code`
   - **Managed pipeline mode**: `Integrated`

#### Configure FastCGI

1. In IIS Manager, select the server (root node)
2. Double-click **FastCGI Settings**
3. Click **Add Application**
4. Set:
   - **Full Path**: `C:\Python311\python.exe`
   - **Arguments**: `C:\Python311\Lib\site-packages\wfastcgi.py`
   - **Environment Variables**: Add `PYTHONPATH=C:\inetpub\wwwroot\prompt_library\src`

### 6. Set Permissions

```powershell
# Grant IIS users access to application directory
icacls "C:\inetpub\wwwroot\prompt_library" /grant "IIS_IUSRS:(OI)(CI)F" /T

# Grant write access to database file
icacls "C:\inetpub\wwwroot\prompt_library\src\prompt_library.db" /grant "IIS_IUSRS:(F)"
```

### 7. Update web.config

Edit `C:\inetpub\wwwroot\prompt_library\src\web.config`:

1. Update Python path if different:

   ```xml
   scriptProcessor="C:\Python311\python.exe|C:\Python311\Lib\site-packages\wfastcgi.py"
   ```

2. Update application path:

   ```xml
   <add key="PYTHONPATH" value="C:\inetpub\wwwroot\prompt_library\src" />
   ```

### 8. Test Deployment

1. In IIS Manager, right-click your site → **Manage Website** → **Browse**
2. The application should load in your browser
3. Test all functionality:
   - Browse prompts
   - Search and filter
   - Customize prompts
   - View analytics

## Troubleshooting

### Issue: "Script must be run as Administrator"

**Solution:**
Right-click PowerShell and select "Run as Administrator", then run the deploy script again.

### Issue: "Python is not found in PATH"

**Solution:**
Install Python 3.8+ and ensure it's added to your system PATH, or specify the full path when running Python commands.

### Issue: PowerShell Script Errors

**Solution:**
Ensure you're using PowerShell 5.1 or later. Run `$PSVersionTable.PSVersion` to check your version.

### Issue: "500 Internal Server Error"

The deploy.ps1 script should prevent this, but if it occurs:

**Check:**

1. Python path in web.config is correct
2. wfastcgi is enabled: `wfastcgi-enable`
3. Permissions on directory: `icacls` command above
4. Check logs: `C:\inetpub\wwwroot\prompt_library\logs\wfastcgi.log`

### Issue: "Module not found" errors

**Solution:**

```powershell
cd C:\inetpub\wwwroot\prompt_library\src
pip install -r requirements.txt
```

### Issue: Database errors

**Solution:**

```powershell
# Recreate database
cd C:\inetpub\wwwroot\prompt_library\src
del prompt_library.db
python load_prompts.py
```

### Issue: Static files not loading

**Check:**

1. Static content is enabled in IIS
2. MIME types are configured in web.config
3. Permissions on static folders

## Maintenance

### Backup Database

```powershell
$date = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item "C:\inetpub\wwwroot\prompt_library\src\prompt_library.db" "C:\backups\prompt_library_$date.db"
```

### Update Application

```powershell
# Stop site in IIS Manager first
# Copy new files
Copy-Item -Path "src\*" -Destination "C:\inetpub\wwwroot\prompt_library\src" -Recurse -Force
# Restart site in IIS Manager
```

### Monitor Logs

```powershell
Get-Content "C:\inetpub\wwwroot\prompt_library\logs\wfastcgi.log" -Tail 50 -Wait
```

## Security Considerations

1. **HTTPS**: Configure SSL certificate in IIS
2. **Authentication**: Add Windows Authentication if needed
3. **Firewall**: Configure Windows Firewall rules
4. **Database**: Regular backups
5. **Updates**: Keep Python and packages updated

## Performance Tuning

1. **Application Pool**: Set appropriate recycling settings
2. **FastCGI**: Increase `maxInstances` in FastCGI settings
3. **Caching**: Enable output caching in IIS
4. **Static Files**: Enable static content compression

## Support

For issues specific to your environment:

1. Check IIS logs: `C:\inetpub\logs\LogFiles`
2. Check application logs: `C:\inetpub\wwwroot\prompt_library\logs`
3. Check Windows Event Viewer for system errors
