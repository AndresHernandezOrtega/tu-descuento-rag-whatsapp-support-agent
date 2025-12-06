# Script para probar Evolution API y generar QR de WhatsApp
# Asegúrate de tener la API corriendo antes de ejecutar este script

# Cargar variables del .env
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.*)$') {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim().Trim('"').Trim('`')
        Set-Variable -Name $name -Value $value -Scope Script
    }
}

$BASE_URL = "http://localhost:8082"
$API_KEY = $EVOLUTION_API_KEY
$INSTANCE_NAME = "whatsapp-bot"

# Función para hacer requests con mejor manejo de errores
function Invoke-EvolutionAPI {
    param(
        [string]$Uri,
        [string]$Method = "Get",
        [string]$Body = $null
    )
    
    $headers = @{
        "apikey" = $API_KEY
        "Content-Type" = "application/json"
    }
    
    try {
        if ($Body) {
            return Invoke-RestMethod -Uri $Uri -Method $Method -Headers $headers -Body $Body -ErrorAction Stop
        } else {
            return Invoke-RestMethod -Uri $Uri -Method $Method -Headers $headers -ErrorAction Stop
        }
    } catch {
        Write-Host "Error en la petición:" -ForegroundColor Red
        Write-Host "  URI: $Uri" -ForegroundColor Gray
        Write-Host "  Status: $($_.Exception.Response.StatusCode.Value__)" -ForegroundColor Gray
        Write-Host "  Message: $($_.Exception.Message)" -ForegroundColor Gray
        return $null
    }
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Testing Evolution API - WhatsApp Connection" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar que la API está corriendo
Write-Host "[1/4] Verificando que Evolution API está corriendo..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/manager/status" -Method Get -Headers @{
        "apikey" = $API_KEY
    } -ErrorAction Stop
    Write-Host "✓ Evolution API está funcionando correctamente" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "✗ Error: Evolution API no está respondiendo" -ForegroundColor Red
    Write-Host "  Asegúrate de que el contenedor esté corriendo: docker-compose ps evolution-api" -ForegroundColor Yellow
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 2. Listar instancias existentes
Write-Host "[2/4] Verificando instancias existentes..." -ForegroundColor Yellow
try {
    $instances = Invoke-RestMethod -Uri "$BASE_URL/instance/fetchInstances" -Method Get -Headers @{
        "apikey" = $API_KEY
    } -ErrorAction Stop
    
    if ($instances -and $instances.Length -gt 0) {
        Write-Host "✓ Instancias encontradas:" -ForegroundColor Green
        foreach ($inst in $instances) {
            Write-Host "  - $($inst.instance.instanceName) | Estado: $($inst.instance.state)" -ForegroundColor Cyan
        }
    } else {
        Write-Host "  No hay instancias creadas" -ForegroundColor Gray
    }
    Write-Host ""
} catch {
    Write-Host "  No se pudieron listar las instancias" -ForegroundColor Yellow
    Write-Host ""
}

# 3. Crear nueva instancia con configuración correcta
Write-Host "[3/4] Creando nueva instancia '$INSTANCE_NAME'..." -ForegroundColor Yellow

$createBody = @{
    instanceName = $INSTANCE_NAME
    qrcode = $true
    integration = "WHATSAPP-BAILEYS"
} | ConvertTo-Json

$createResponse = Invoke-EvolutionAPI -Uri "$BASE_URL/instance/create" -Method Post -Body $createBody

if ($createResponse) {
    if ($createResponse.instance) {
        Write-Host "✓ Instancia creada exitosamente" -ForegroundColor Green
        Write-Host "  Instance Name: $($createResponse.instance.instanceName)" -ForegroundColor Cyan
        if ($createResponse.instance.instanceId) {
            Write-Host "  Instance ID: $($createResponse.instance.instanceId)" -ForegroundColor Cyan
        }
        Write-Host ""
    } else {
        Write-Host "  La instancia '$INSTANCE_NAME' ya existe o ya está creada" -ForegroundColor Yellow
        Write-Host ""
    }
} else {
    Write-Host "  Continuando con la instancia existente..." -ForegroundColor Yellow
    Write-Host ""
}

# 4. Conectar y obtener QR
Write-Host "[4/4] Conectando a WhatsApp y generando QR..." -ForegroundColor Yellow
Write-Host ""

# Primero intentar obtener el estado actual
$stateResponse = Invoke-EvolutionAPI -Uri "$BASE_URL/instance/connectionState/$INSTANCE_NAME" -Method Get

if ($stateResponse -and $stateResponse.instance.state -eq "open") {
    Write-Host "✓ ¡La instancia ya está conectada a WhatsApp!" -ForegroundColor Green
    Write-Host "  Estado: $($stateResponse.instance.state)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "No es necesario escanear el QR nuevamente." -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "IMPORTANTE: Escanea el QR con tu WhatsApp" -ForegroundColor Green
    Write-Host "1. Abre WhatsApp en tu teléfono" -ForegroundColor Cyan
    Write-Host "2. Toca Menú o Configuración" -ForegroundColor Cyan
    Write-Host "3. Toca Dispositivos vinculados" -ForegroundColor Cyan
    Write-Host "4. Toca 'Vincular un dispositivo'" -ForegroundColor Cyan
    Write-Host "5. Apunta tu teléfono a esta pantalla para escanear el código" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Generando QR Code..." -ForegroundColor Yellow
    Write-Host ""

    # Conectar a WhatsApp (esto genera el QR)
    $connectResponse = Invoke-EvolutionAPI -Uri "$BASE_URL/instance/connect/$INSTANCE_NAME" -Method Get

    if ($connectResponse) {
        Start-Sleep -Seconds 2
        
        # Abrir el navegador con el QR
        Write-Host "==================================================" -ForegroundColor Green
        Write-Host "  ABRIENDO NAVEGADOR CON QR CODE" -ForegroundColor Green
        Write-Host "==================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "URL del QR:" -ForegroundColor Cyan
        Write-Host "  http://localhost:8082/instance/qrcode/$INSTANCE_NAME" -ForegroundColor Yellow
        Write-Host ""
        
        Start-Process "http://localhost:8082/instance/qrcode/$INSTANCE_NAME"
        
        Write-Host "El QR expira en 30 segundos. Si no lo escaneas a tiempo," -ForegroundColor Yellow
        Write-Host "ejecuta este script nuevamente." -ForegroundColor Yellow
        Write-Host ""
        
        # Monitorear el estado de conexión
        Write-Host "Monitoreando estado de conexión (presiona Ctrl+C para cancelar)..." -ForegroundColor Gray
        Write-Host ""
        
        $timeout = 0
        $maxTimeout = 30
        
        while ($timeout -lt $maxTimeout) {
            Start-Sleep -Seconds 2
            $timeout += 2
            
            $currentState = Invoke-EvolutionAPI -Uri "$BASE_URL/instance/connectionState/$INSTANCE_NAME" -Method Get
            
            if ($currentState -and $currentState.instance.state -eq "open") {
                Write-Host ""
                Write-Host "==================================================" -ForegroundColor Green
                Write-Host "  ✓ ¡CONECTADO EXITOSAMENTE!" -ForegroundColor Green
                Write-Host "==================================================" -ForegroundColor Green
                Write-Host ""
                break
            }
            
            Write-Host "." -NoNewline -ForegroundColor Gray
        }
        
        if ($timeout -ge $maxTimeout) {
            Write-Host ""
            Write-Host ""
            Write-Host "⏱ Tiempo de espera agotado." -ForegroundColor Yellow
            Write-Host "Si no escaneaste el QR, ejecuta el script nuevamente." -ForegroundColor Yellow
            Write-Host ""
        }
    } else {
        Write-Host "✗ No se pudo iniciar la conexión" -ForegroundColor Red
        Write-Host ""
        Write-Host "Intenta acceder manualmente al manager:" -ForegroundColor Yellow
        Write-Host "  http://localhost:8082/manager" -ForegroundColor Cyan
        Write-Host ""
    }
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  URLs Útiles:" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "QR Code:        http://localhost:8082/instance/qrcode/$INSTANCE_NAME" -ForegroundColor White
Write-Host "Estado:         http://localhost:8082/instance/connectionState/$INSTANCE_NAME" -ForegroundColor White
Write-Host "Swagger Docs:   http://localhost:8082/api-docs" -ForegroundColor White
Write-Host ""
Write-Host "Para ver los logs del contenedor:" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f evolution-api" -ForegroundColor Cyan
Write-Host ""
